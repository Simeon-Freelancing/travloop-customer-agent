from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field

class SearchSimilarTripsInput(BaseModel):
    destination: str
    start_date: date
    end_date: date
    trip_type: Optional[str] = Field(
        None, description="General trip type, e.g., leisure, group"
    )

class TripSummary(BaseModel):
    trip_id: str
    trip_name: str
    start_date: date
    end_date: date
    trip_url: str

class SearchSimilarTripsOutput(BaseModel):
    similar_trips: List[TripSummary]


class CreateTravelRequestInput(BaseModel):
    user_id: str
    destination_raw: str
    destination_normalized: str
    travel_window_start: date
    travel_window_end: date
    date_flexibility: str  # fixed, ±3 days, ±1 week
    budget_band: str        # budget, mid-range, premium
    travel_style: str       # vacation, adventure, cultural, relaxed
    group_openness: str     # open to group, maybe, solo
    source: str             # AI_NO_RESULTS or AI_DISCOVERY

class CreateTravelRequestOutput(BaseModel):
    request_id: str
    status: str  # PENDING_REVIEW, MATCHED, etc.


class GetUserContextInput(BaseModel):
    user_id: str

class PreviousTrip(BaseModel):
    trip_id: str
    destination: str
    start_date: date
    end_date: date

class GetUserContextOutput(BaseModel):
    user_id: str
    past_trips: List[PreviousTrip]
    preferred_destinations: List[str]