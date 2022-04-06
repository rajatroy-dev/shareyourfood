from shareyourfood.bot.constants import Constants
from shareyourfood.bot.conversation import Conversation
from shareyourfood.data.repository import Repository


class Handle:
    def __init__(self) -> None:
        self.conversation: Conversation = Conversation()
        self.repository: Repository = Repository()

    def introduction(self, chat_id: int, full_name: str) -> None:
        self.conversation.introduce(chat_id=chat_id,
                                    full_name=full_name)

    def share(self, chat_id: int, username: str, message_id: int) -> None:
        self.repository.save_share_food_details(chat_id=chat_id,
                                                username=username,
                                                message_id=message_id)
        self.conversation.ask_location_for_share(chat_id)

    def request(self, chat_id: int, username: str, message_id: int) -> None:
        self.repository.save_request_food_details(chat_id=chat_id,
                                                  username=username,
                                                  message_id=message_id)
        self.conversation.ask_location_for_request(chat_id)

    def location(self, chat_id: int, username: str, message_id: int, latitude: float, longitude: float) -> None:
        entry_search_result = self.repository.find_entry(chat_id=chat_id,
                                                         username=username,
                                                         message_id=message_id - 2)

        if entry_search_result \
                and entry_search_result.message_type == Constants.SHARE:
            self.repository.save_share_food_details(chat_id=chat_id,
                                                    username=username,
                                                    message_id=message_id - 2,
                                                    latitude=latitude,
                                                    longitude=longitude)
            self.conversation.reply_shared_details_saved(chat_id)

        elif entry_search_result \
                and entry_search_result.message_type == Constants.REQUEST:
            food_search_result = self.repository.find_food(latitude=latitude,
                                                           longitude=longitude)
            if not food_search_result:
                self.conversation.no_share_found(chat_id)
            else:
                self.conversation.reply_nearby_shares(chat_id=chat_id,
                                                      shares=food_search_result)

        else:
            self.conversation.unknown_location(chat_id)
