from mcp.client.streamable_http import streamable_http_client
from contextlib import AsyncExitStack
from mcp import ClientSession
from typing import Optional
from langchain.chat_models import BaseChatModel
from langchain_openai import AzureOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
import logging


class Agent:
    def __init__(self, llm):
        self.llm: BaseChatModel = llm
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.logger = logging.getLogger(__name__)
        self.tools = []

    async def connect_to_mcp_server(self, base_url: str):
        try:
            self._streams_context = streamable_http_client(url=base_url)
            read_stream, write_stream, _ = await self.exit_stack.enter_async_context(self._streams_context)

            self._session_context = ClientSession(read_stream, write_stream)
            self.session = await self.exit_stack.enter_async_context(self._session_context)

            await self.session.initialize()
            
            # List available tools
            response = await self.session.list_tools()
            self.tools = response.tools
            print("\nConnected to server with tools:", [tool.name for tool in self.tools])
        except Exception as e:
            self.logger.error(f"Failed to connect to MCP server: {e}")
            await self.exit_stack.aclose()
            raise

    def make_mcp_tool(self, tool):
        async def call_tool(**kwargs):
            return await self.session.call_tool(tool.name, kwargs)

        return StructuredTool.from_function(
            name=tool.name,
            description=tool.description,
            coroutine=call_tool
        )

    async def process_query(self, user_query, invoked_tools=[]):
        try:
            self.logger.info(f"Processing query: {user_query}")
            self.messages = [{"role": "user", "content": user_query}]
           
            mcp_tools = [self.make_mcp_tool(tool) for tool in self.tools]
            
            while True:
                content = f"""
                        Hello welcome to travloop ai agent, 
                        I have access to {len(self.tools)} tools:
                        """ 
                response = {
                    "content": content
                }
                if not response.get("tool_calls") and response.get("content"):
                    self.messages.append({"role": "assistant", "content": response["content"]})
                    return self.messages
                
                if tool_calls := response.get("tool_calls"):
                    for tool_call in tool_calls:
                        tool_args = tool_call['args'] 
                        tool_name = tool_call['name'] 
                        tool_id = tool_call['id']
                        
                        if tool_name not in invoked_tools:
                            result = await self.session.call_tool(tool_name, tool_args)
                            invoked_tools.append(str(tool_name))  
                            self.messages.append(
                                {"role": "tool", 
                                "content": result, 
                                "tool_call_id": tool_id
                                })
                            self.logger.info(f"Tool {tool_name} result: {result}...")
                break

        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            raise
        finally:
            await self.exit_stack.aclose()
    
    @staticmethod
    async def get_llm(model_name: str) -> BaseChatModel:
        if model_name == "Azure Openai":
            return AzureOpenAI(model_name="gpt-3.5-turbo-instruct")
        elif model_name == "Gemini":
            return ChatGoogleGenerativeAI(model_name="gemini-2.0-flash")