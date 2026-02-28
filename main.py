from fastapi import FastAPI
from fake_api import router as mock_router
from travloop_mcp.server import mcp
from pydantic import BaseModel
from agent.app.agent import Agent


app = FastAPI(title="Mock API Server")

app.include_router(mock_router, prefix="/api")

class AgentRequest(BaseModel):
    message: str

@app.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    agent = Agent(llm="Gemini")
    await agent.connect_to_mcp_server("http://127.0.0.1:8001/mcp")
    messages = await agent.process_query(request.message)

    return {"response":messages[-1], 
            "actions_taken": [message for message in messages if message["role"]=="tool"]}