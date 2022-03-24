import os

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from constants import Constants
from validations import Validate


class Conversation:
    def __init__(self, bot: Bot, chat_id: int) -> None:
        self.bot = bot
        self.chat_id = chat_id

    def introduce(self):
        Validate.chat_id(self.chat_id)
        self.bot.send_message(chat_id=self.chat_id,
                              text=Constants.INTRODUCTION,
                              reply_markup=ReplyKeyboardRemove())

    def request_location(self):
        Validate.chat_id(self.chat_id)

        location_keyboard = KeyboardButton(
            text="Share location", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        self.bot.send_message(chat_id=self.chat_id,
                              text=Constants.REQUEST_LOCATION,
                              reply_markup=reply_markup)
