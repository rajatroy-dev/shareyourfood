from shareyourfood.bot.constants import Constants
from shareyourfood.data.dao.cosmos_db.cosmos import Cosmos as Dao
from shareyourfood.data.model.entry import Entry
from shareyourfood.data.model.location import PointLocation


class Repository:
    def __init__(self) -> None:
        self.dao = Dao()

    def save_share_food_details(self, chat_id: int, username: str, message_id: int, latitude: float = 0.0, longitude: float = 0.0, type: str = Constants.SHARE):
        location: PointLocation = PointLocation([latitude, longitude])
        entry: Entry = Entry(id='',
                             message_type=type,
                             entry_id='',
                             chat_id=chat_id,
                             username=username,
                             message_id=message_id,
                             location=location)
        self.dao.save_entry(entry)

    def find_entry(self, chat_id: int, username: str, message_id: int):
        self.dao.find_entry(chat_id=chat_id,
                            username=username,
                            message_id=message_id)

    def save_request_food_details(self, chat_id: int, username: str, message_id: int, type: str = Constants.REQUEST):
        entry: Entry = Entry(id='',
                             message_type=type,
                             entry_id='',
                             chat_id=chat_id,
                             username=username,
                             message_id=message_id,
                             location=None)
        self.dao.save_entry(entry)

    def find_food(self, latitude: float, longitude: float):
        self.dao.find_food(latitude=latitude, longitude=longitude)
