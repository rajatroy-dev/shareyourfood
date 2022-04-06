# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = location_from_dict(json.loads(json_string))

from typing import List, Any

from shareyourfood.data.model.conversion import from_float, from_list, from_str, to_class, to_float


class Location:
    type: str
    coordinates: List[float]

    def __init__(self, type: str, coordinates: List[float]) -> None:
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        coordinates = from_list(from_float, obj.get("coordinates"))
        return Location(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["coordinates"] = from_list(to_float, self.coordinates)
        return result


def location_from_dict(s: Any) -> Location:
    return Location.from_dict(s)


def location_to_dict(x: Location) -> Any:
    return to_class(Location, x)
