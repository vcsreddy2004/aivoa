# app/schema.py
from pydantic import BaseModel
from typing import List

class HCPInput(BaseModel):
    text: str

class HCPOutput(BaseModel):
    hcp_name: str
    interaction_type: str
    date: str
    time: str
    attendees: List[str]
    topics: str
    materials: str
    samples: str
    sentiment: str
    outcomes: str
    follow_up: str