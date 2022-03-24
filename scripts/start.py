import os

import azure.functions as func
from telegram import Bot, Update


class Start:
    def __init__(self, req: func.HttpRequest) -> None:
        self.token: str = os.getenv('TOKEN')
        self.bot: Bot = Bot(self.token)
        self.update: Update = Update.de_json(req.get_json(), self.bot)

    def bot(self) -> None:
        pass
