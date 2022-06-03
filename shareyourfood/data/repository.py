from typing import Any, Dict, Iterable
from shareyourfood.bot.constants import Constants
from shareyourfood.data.dao.cosmos_db.cosmos import Cosmos as Dao
from shareyourfood.data.model.entry import Entry
from shareyourfood.data.model.location import PointLocation


class Repository:
    def __init__(self) -> None:
        self.dao: Dao = Dao()

    def save_share_food_details(self, chat_id: int, username: str, message_id: int, latitude: float = 0.0, longitude: float = 0.0, type: str = Constants.SHARE) -> bool:
        location: PointLocation = PointLocation([latitude, longitude])
        entry: Entry = Entry(id='',
                             message_type=type,
                             entry_id='',
                             chat_id=chat_id,
                             username=username,
                             message_id=message_id,
                             location=location)
        response: bool = self.dao.save_entry(entry)
        return response

    def save_request_food_details(self, chat_id: int, username: str, message_id: int, type: str = Constants.REQUEST) -> bool:
        entry: Entry = Entry(id='',
                             message_type=type,
                             entry_id='',
                             chat_id=chat_id,
                             username=username,
                             message_id=message_id,
                             location=None)
        response: bool = self.dao.save_entry(entry)
        return response

    def find_entry(self, chat_id: int, username: str, message_id: int) -> Dict[str, Any]:
        response: Dict[str, Any] = self.dao.find_entry(chat_id=chat_id,
                                                       username=username,
                                                       message_id=message_id)
        return response

    def find_food(self, latitude: float, longitude: float) -> Iterable[Dict[str, Any]]:
        response: Iterable[Dict[str, Any]] = self.dao.find_food(
            latitude=latitude, longitude=longitude)
        return response
