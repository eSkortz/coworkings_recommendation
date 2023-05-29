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

PlaceId = int

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Place:
    id: PlaceId
    name: str
    type: str
    price: int
    stop_price: Optional[int] = None
    seats_count: Optional[int] = None

CoworkingId = int

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Coworking:
    id: CoworkingId
    name: str
    coordinates: GeoCoords
    tags: List[Tag]
    undergrounds: List[MetroStation]
    places: List[Place]
    review_rate: float
    review_count: int
    rates_count: int
    opening_hours: OpeningHours

    @property
    def avg_price_per_workplace(self) -> float:
        def avg_price(place: Place) -> float:
            seats_count = place.seats_count or 1
            return place.price / seats_count
        
        return sum(map(avg_price, self.places)) / len(self.places)