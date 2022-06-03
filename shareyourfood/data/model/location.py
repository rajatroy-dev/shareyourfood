# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = location_from_dict(json.loads(json_string))

from typing import Dict, List, Any

from shareyourfood.data.model.conversion import from_float, from_list, to_class, to_float


class PointLocation:
    type: str
    coordinates: List[float]

    def __init__(self, coordinates: List[float]) -> None:
        self.type = 'Point'
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> 'PointLocation':
        assert isinstance(obj, Dict)
        coordinates = from_list(from_float, obj.get("coordinates"))
        return PointLocation(coordinates)

    def to_dict(self) -> Dict:
        result: Dict = {}
        result["type"] = 'Point'
        result["coordinates"] = from_list(to_float, self.coordinates)
        return result


def location_from_dict(s: Any) -> PointLocation:
    return PointLocation.from_dict(s)


def location_to_dict(x: PointLocation) -> Any:
    return to_class(PointLocation, x)
