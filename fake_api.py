import json
from pathlib import Path
from dataclasses import  dataclass
from typing import Optional
from fastapi import APIRouter

router = APIRouter()

BASE_DIR = Path(__file__).parent / "./mock_data"
def load_json(filename):
    with open(BASE_DIR / filename, "r") as f:
        return json.load(f)


@router.get("/trips")
def get_trips_search(location: str = None, startDate: str = None, endDate: str = None, guests: int = 1):
    """
    Used by: search_similar_trips
    Logic: Returns raw trips; MCP tool will then apply '2 of 3' similarity rule.
    """
    return load_json("trips.json")

@router.get("/trips/booked/{user_email}")
def get_booked_trips(user_email: str):
    """
    Used by: get_user_context
    Source: API Doc 'getUserBookedTrips'
    """
    return load_json("booked_trips.json")

@router.get("/trips/custom/{user_email}")
def get_custom_trips(user_email: str):
    """
    Used by: get_user_context
    Source: API Doc 'getUserCustomTrips'
    """
    return load_json("custom_trips.json")

@router.get("/trips/memberships/{user_email}")
def get_user_memberships(user_email: str):
    """
    Used by: get_user_context
    Source: API Doc 'getTripMembershipsWithDetails'
    Provides the broader context of what user has joined.
    """
    return load_json("memberships.json")

@router.post("/travel-requests")
def create_travel_request(user_id: int,
                          destination_raw: str,
                          destination_normalized: str,
                          travel_style: str,  # Vacation, Adventure, Cultural, Relaxed
                          budget_band: str,   # Budget, Mid-range, Premium
                          date_flexibility: str,  # Fixed, ±3 days, ±1 week
                          group_openness: str,  # Open to group, Maybe, Solo
                          start_date: Optional[str],
                          end_date: Optional[str]):
    # In a real app, this would save to a 'travel_requests' or 'custom_trips' table
    return {
        "status": "success",
        "request_id": "REQ-12345",
        "message": "Thanks! This is a travel request, not a confirmed booking. We'll notify you if a matching trip becomes available."
    }