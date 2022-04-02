# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = share_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any

from shareyourfood.data.model.conversion import from_float, to_float


@dataclass
class Location:
    latitude: float
    longitude: float

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        return Location(latitude, longitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        return result
