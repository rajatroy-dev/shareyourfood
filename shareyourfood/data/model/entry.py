# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = share_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any

from shareyourfood.data.model.conversion import from_int, from_str, to_class
from shareyourfood.data.model.location import Location


@dataclass
class Entry:
    id: str
    message_type: str
    entry_id: str
    chat_id: int
    username: str
    message_id: int
    location: Location

    @staticmethod
    def from_dict(obj: Any) -> 'Entry':
        assert isinstance(obj, dict)
        id = from_str(obj.get("_id"))
        message_type = from_str(obj.get("message_type"))
        entry_id = from_str(obj.get("entry_id"))
        chat_id = from_int(obj.get("chat_id"))
        username = from_str(obj.get("username"))
        message_id = from_int(obj.get("message_id"))
        location = Location.from_dict(obj.get("location"))
        return Entry(id, message_type, entry_id, chat_id, username, message_id, location)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_id"] = from_str(self.id)
        result["message_type"] = from_str(self.message_type)
        result["entry_id"] = from_str(self.entry_id)
        result["chat_id"] = from_int(self.chat_id)
        result["username"] = from_str(self.username)
        result["message_id"] = from_int(self.message_id)
        result["location"] = to_class(Location, self.location)
        return result


def share_from_dict(s: Any) -> Entry:
    return Entry.from_dict(s)


def share_to_dict(x: Entry) -> Any:
    return to_class(Entry, x)