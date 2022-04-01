from telegram import Bot, KeyboardButton, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove

from shareyourfood.bot.constants import Constants
from shareyourfood.bot.validations import Validate


class Conversation:
    def __init__(self, bot: Bot, chat_id: int) -> None:
        self.bot = bot
        self.chat_id = chat_id
        Validate.chat_id(self.chat_id)

    def introduce(self, full_name):
        self.bot.send_message(chat_id=self.chat_id,
                              text=f'Hi! <b>{full_name}</b> &#128075;, {Constants.INTRODUCTION}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def request_start(self):
        pass

    def request_location(self):
        location_keyboard = KeyboardButton(
            text="Share location", request_location=True)
        custom_keyboard = [[location_keyboard]]
        reply_markup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        self.bot.send_message(chat_id=self.chat_id,
                              text=Constants.REQUEST_LOCATION,
                              reply_markup=reply_markup)

    def request_find_people_near_you(self):
        pass
