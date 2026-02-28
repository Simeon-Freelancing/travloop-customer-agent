from fastmcp import FastMCP
from .tools import search_similar_trips, create_travel_request, get_user_context
from .logger import logger
import sys

mcp = FastMCP("travloop_server", json_response=False, stateless_http=False)

@mcp.tool()
async def search_similar_trips_tool(destination: str, start_date: str, end_date: str, trip_type: str = None):
    """Search for similar trips"""
    from .tool_schemas import SearchSimilarTripsInput
    result = await search_similar_trips(SearchSimilarTripsInput(destination=destination, start_date=start_date, end_date=end_date, trip_type=trip_type))
    return result.model_dump()

@mcp.tool()
async def create_travel_request_tool(user_id: str, destination_raw: str, destination_normalized: str, travel_window_start: str, travel_window_end: str, date_flexibility: str, budget_band: str, travel_style: str, group_openness: str, source: str):
    """Create a travel request"""
    from .tool_schemas import CreateTravelRequestInput
    result = await create_travel_request(CreateTravelRequestInput(user_id=user_id, destination_raw=destination_raw, destination_normalized=destination_normalized, travel_window_start=travel_window_start, travel_window_end=travel_window_end, date_flexibility=date_flexibility, budget_band=budget_band, travel_style=travel_style, group_openness=group_openness, source=source))
    return result.model_dump()


@mcp.tool()
async def get_user_context_tool(user_id: str):
    """Get user context and history"""
    from .tool_schemas import GetUserContextInput
    result = await get_user_context(GetUserContextInput(user_id=user_id))
    return result.model_dump()

# if __name__ == "__main__":
#     try:
#         logger.info("Starting MCP server with stdio transport...")
#         mcp.run(transport="stdio")
#     except Exception as e:
#         logger.critical(f"Fatal error in MCP server: {e}", exc_info=True)
#         sys.exit(1)
#     finally:
#         logger.info("MCP server shutting down")
app = mcp.http_app(transport="streamable-http")