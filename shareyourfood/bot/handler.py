from typing import Any, Dict, Iterable
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

    def unknown_message(self, chat_id: int) -> None:
        self.conversation.bot_did_not_understand(chat_id=chat_id)

    def share(self, chat_id: int, username: str, message_id: int) -> None:
        response: bool = self.repository.save_share_food_details(chat_id=chat_id,
                                                                 username=username,
                                                                 message_id=message_id)
        if response:
            self.conversation.ask_location_for_share(chat_id)
        else:
            self.conversation.reply_server_error(chat_id)

    def request(self, chat_id: int, username: str, message_id: int) -> None:
        response: bool = self.repository.save_request_food_details(chat_id=chat_id,
                                                                   username=username,
                                                                   message_id=message_id)
        if response:
            self.conversation.ask_location_for_request(chat_id)
        else:
            self.conversation.reply_server_error(chat_id)

    def location(self, chat_id: int, username: str, message_id: int, latitude: float, longitude: float) -> None:
        entry_search_result: Dict[str, Any] = self.repository.find_entry(chat_id=chat_id,
                                                                         username=username,
                                                                         message_id=message_id - 2)

        if entry_search_result \
                and entry_search_result['message_type'] == Constants.SHARE:
            response: bool = self.repository.save_share_food_details(chat_id=chat_id,
                                                                     username=username,
                                                                     message_id=message_id,
                                                                     latitude=latitude,
                                                                     longitude=longitude)
            if response:
                self.conversation.reply_shared_details_saved(chat_id)
            else:
                self.conversation.reply_server_error(chat_id)

        elif entry_search_result \
                and entry_search_result['message_type'] == Constants.REQUEST:
            food_search_result: Iterable[Dict[str, Any]] = self.repository.find_food(latitude=latitude,
                                                                                     longitude=longitude)
            if food_search_result:
                self.conversation.reply_nearby_shares(chat_id=chat_id,
                                                      shares=food_search_result)
            else:
                self.conversation.no_share_found(chat_id)

        else:
            self.conversation.unknown_location(chat_id)
