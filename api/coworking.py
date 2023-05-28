from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined
from typing import List, Optional

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpeningHoursDay:
    time: str

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OpeningHours:
    mon: OpeningHoursDay
    tue: OpeningHoursDay
    wed: OpeningHoursDay
    thu: OpeningHoursDay
    fri: OpeningHoursDay
    sat: OpeningHoursDay
    sun: OpeningHoursDay

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Tag:
    id: str
    comment: Optional[str] = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MetroStation:
    name: str
    line: str
    walking_time: int

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GeoCoords:
    lat: float
    lon: float

CoworkingId = int

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Coworking:
    id: CoworkingId
    name: str
    coordinates: GeoCoords
    tags: List[Tag]
    undergrounds: List[MetroStation]
    review_rate: float
    review_count: int
    rates_count: int
    opening_hours: OpeningHours