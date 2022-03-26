import os
import re

import azure.functions as func
from telegram import Bot, Update

from shareyourfood.bot.conversation import Conversation


class Start:
    def __init__(self, req: func.HttpRequest) -> None:
        self.token: str = os.getenv('TOKEN')
        self.bot: Bot = Bot(self.token)
        self.update: Update = Update.de_json(req.get_json(), self.bot)
        self.conversion: Conversation = Conversation(self.bot, self.update.effective_chat.id)

    def chat(self) -> None:
        if re.search("^/start$", self.update.message.text):
            self.conversion.introduce()
        else:
            self.conversion.introduce()
