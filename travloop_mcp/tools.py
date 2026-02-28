from .tool_schemas import *
import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

async def search_similar_trips(input_data: SearchSimilarTripsInput) -> SearchSimilarTripsOutput:
    """
    MCP Tool: Search for up to 3 trips similar to the given criteria.
    Logic to query Travloop API will be implemented externally.
    """
    result = requests.get(f"{BASE_URL}/api/trips/search", params={
        "location": input_data.destination,  
        "start_date": input_data.start_date,
        "end_date": input_data.end_date
    })
    trips = [TripSummary(**trip) for trip in result.json()[:3]]  # Limit to 3
    return SearchSimilarTripsOutput(similar_trips=trips)

async def create_travel_request(input_data: CreateTravelRequestInput) -> CreateTravelRequestOutput:
    """
    MCP Tool: Create a structured travel request.
    Travloop API integration will be handled externally.
    """
    # Placeholder return
    response = requests.post(f"{BASE_URL}/api/travel-requests", json={
        "user_id": input_data.user_id,
        "destination_raw": input_data.destination_raw,
        "destination_normalized": input_data.destination_normalized,
        "travel_style": input_data.travel_style,
        "budget_band": input_data.budget_band,
        "date_flexibility": input_data.date_flexibility,
        "group_openness": input_data.group_openness,
        "start_date": input_data.travel_window_start.isoformat(),
        "end_date": input_data.travel_window_end.isoformat()
    })
    return CreateTravelRequestOutput(request_id=response.json()["request_id"], status="PENDING_REVIEW")


async def get_user_context(input_data: GetUserContextInput) -> GetUserContextOutput:
    """Return user profile context including past trips and preferences."""
    try:
        trips_data = requests.get(f"{BASE_URL}/api/trips/booked/{input_data.user_id}").json()
        custom_trips_data = requests.get(f"{BASE_URL}/api/trips/custom/{input_data.user_id}").json()
        memberships_data = requests.get(f"{BASE_URL}/api/trips/memberships/{input_data.user_id}").json()

        # Parse trips
        past_trips = [PreviousTrip(trip_id=t.get("trip_id", ""), destination=t.get("destination", ""), 
                                   start_date=date.fromisoformat(t.get("start_date")), 
                                   end_date=date.fromisoformat(t.get("end_date"))) 
                     for t in trips_data.get("trips", [])]
        
        # Extract preferred destinations
        preferred = [m.get("destination") for m in memberships_data.get("memberships", []) if m.get("destination")]

        return GetUserContextOutput(user_id=input_data.user_id, past_trips=past_trips, preferred_destinations=preferred)
    except Exception as e:
        print(f"Error in get_user_context: {e}")
        return GetUserContextOutput(user_id=input_data.user_id, past_trips=[], preferred_destinations=[])
