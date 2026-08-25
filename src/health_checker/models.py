from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Website:
    id: str
    url: str
    description: Optional[str]

@dataclass
class PhoneNumber:
    id: str
    number: str
    extension: Optional[float]
    description: str

@dataclass
class Category:
    id: str
    name: str
    description: str
    sortNumber: float

@dataclass
class Resource:
    id: str
    name: str
    description: str
    search_description: str
    url_slug: str
    in_operation: str
    hours: str
    claimed_by_owner: bool
    verified_for_accurate_info: bool
    last_verified_on: datetime
    updated_at: datetime
    created_at: datetime

@dataclass
class Entry(Resource):
    websites: list[Website] = field(default_factory=list)
    categories: list[Category] = field(default_factory=list)
    phone_numbers: list[PhoneNumber] = field(default_factory=list)

