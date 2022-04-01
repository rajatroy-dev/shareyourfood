import os
import re

import azure.functions as func
from telegram import Bot, Update

from shareyourfood.bot.conversation import Conversation
from shareyourfood.data.repository import Repository


class Start:
    def __init__(self, req: func.HttpRequest) -> None:
        self.token: str = os.getenv('TOKEN')
        self.bot: Bot = Bot(self.token)
        self.update: Update = Update.de_json(req.get_json(), self.bot)
        self.chat_id: int = self.update.effective_chat.id
        self.username: str = self.update.effective_chat.username
        self.full_name: str = self.update.effective_chat.full_name
        self.message_id: int = self.update.effective_message.message_id
        self.conversion: Conversation = Conversation(self.bot, self.update.effective_chat.id)
        self.repository: Repository = Repository()

    def chat(self) -> None:
        if self.update.effective_message.text and re.search("^/start$", self.update.message.text):
            self.conversion.introduce(self.full_name)
        elif self.update.effective_message.text and re.search("^/share$", self.update.message.text):
            self.repository.share_food(self.message_id, self.username)
            self.conversion.request_location()
        elif self.update.effective_message.text and re.search("^/request$", self.update.message.text):
            self.repository.request_food(self.message_id, self.username)
            self.conversion.request_location()
        elif self.update.effective_message.location and self.update.effective_message.location.latitude and self.update.effective_message.location.longitude:
            pass
        else:
            self.conversion.introduce(self.full_name)
