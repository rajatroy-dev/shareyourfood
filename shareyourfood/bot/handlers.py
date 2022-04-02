from shareyourfood.bot.constants import Constants
from shareyourfood.bot.conversation import Conversation
from shareyourfood.data.model.location import Location
from shareyourfood.data.repository import Repository


class Handle:
    def __init__(self) -> None:
        self.conversation: Conversation = Conversation()
        self.repository: Repository = Repository()

    def introduction(self, chat_id: int, full_name: str) -> None:
        self.conversation.introduce(chat_id, full_name)

    def share(self, chat_id: int, username: str, message_id: int) -> None:
        self.repository.share_food(chat_id, username, message_id)
        self.conversation.location_for_share(chat_id)

    def request(self, chat_id: int, username: str, message_id: int) -> None:
        self.repository.request_food(chat_id, username, message_id)
        self.conversation.location_for_request(chat_id)

    def location(self, chat_id: int, username: str, message_id: int, latitude: float, longitude: float) -> None:
        entry_search_result = self.repository.find_entry(
            chat_id, username, message_id - 1)

        if entry_search_result \
                and entry_search_result.message_type == Constants.SHARE:
            location: Location = Location(latitude, longitude)
            self.repository.share_food(
                chat_id, username, message_id - 1, location)
            self.conversation.shared_details_saved(chat_id)

        elif entry_search_result \
                and entry_search_result.message_type == Constants.REQUEST:
            location: Location = Location(latitude, longitude)
            food_search_result = self.repository.find_food(location)
            if not food_search_result:
                self.conversation.no_share_found(chat_id)
            else:
                pass

        else:
            self.conversation.unknown_location(chat_id)
