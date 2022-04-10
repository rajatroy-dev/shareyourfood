import os
import re

import azure.functions as func
from telegram import Bot, Update

from shareyourfood.bot.handler import Handle


class Start:
    def __init__(self, req: func.HttpRequest) -> None:
        self.token: str = os.getenv('TOKEN')
        self.bot: Bot = Bot(self.token)

        self.update: Update = Update.de_json(req.get_json(), self.bot)
        self.chat_id: int = self.update.effective_chat.id
        self.username: str = self.update.effective_chat.username
        self.full_name: str = self.update.effective_chat.full_name
        self.message_id: int = self.update.effective_message.message_id

        self.handle: Handle = Handle()

    def chat(self) -> None:
        if self.update.effective_message.text \
                and re.search('^/start$', self.update.message.text):
            self.handle.introduction(chat_id=self.chat_id,
                                     full_name=self.full_name)

        elif self.update.effective_message.text \
                and re.search('^/share$', self.update.message.text):
            self.handle.share(chat_id=self.chat_id,
                              username=self.username,
                              message_id=self.message_id)

        elif self.update.effective_message.text \
                and re.search('^/request$', self.update.message.text):
            self.handle.request(chat_id=self.chat_id,
                                username=self.username,
                                message_id=self.message_id)

        elif self.update.effective_message.location \
                and self.update.effective_message.location.latitude \
                and self.update.effective_message.location.longitude:
            self.handle.location(chat_id=self.chat_id,
                                 username=self.username,
                                 message_id=self.message_id,
                                 latitude=self.update.effective_message.location.latitude,
                                 longitude=self.update.effective_message.location.longitude)

        else:
            self.handle.introduction(chat_id=self.chat_id,
                                     full_name=self.full_name)
