from shareyourfood.bot.constants import Constants
from shareyourfood.data.model.location import Location


class Repository:
    def save_share_food_details(self, chat_id: int, username: str, message_id: int, location: Location = None, type: str = Constants.SHARE):
        pass

    def find_entry(self, chat_id: int, username: str, message_id: int):
        pass

    def save_request_food_details(self, chat_id: int, username: str, message_id: int, type: str = Constants.REQUEST):
        pass

    def find_food(self, location: Location):
        pass
