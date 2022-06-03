import os
from typing import Any, Dict, Iterable, List
from telegram import Bot, KeyboardButton, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove

from shareyourfood.bot.constants import Constants


class Conversation:
    def __init__(self) -> None:
        self.token: str = os.getenv('TOKEN')
        self.bot: Bot = Bot(self.token)

    def introduce(self, chat_id: int, full_name: str) -> None:
        self.bot.send_message(chat_id=chat_id,
                              text=f'Hi! <b>{full_name}</b> &#128075;, {Constants.INTRODUCTION}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def ask_location_for_share(self, chat_id: int) -> None:
        location_keyboard: KeyboardButton = KeyboardButton(
            text='Share location', request_location=True)
        custom_keyboard: List[List[KeyboardButton]] = [[location_keyboard]]
        reply_markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        self.bot.send_message(chat_id=chat_id,
                              text=Constants.SHARE_LOCATION,
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)

    def ask_location_for_request(self, chat_id: int) -> None:
        location_keyboard: KeyboardButton = KeyboardButton(
            text='Share location', request_location=True)
        custom_keyboard: List[List[KeyboardButton]] = [[location_keyboard]]
        reply_markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        self.bot.send_message(chat_id=chat_id,
                              text=Constants.REQUEST_LOCATION,
                              reply_markup=reply_markup)

    def unknown_location(self, chat_id: int) -> None:
        self.bot.send_message(chat_id=chat_id,
                              text=f'Sorry! &#128531; {Constants.UNKOWN_LOCATION}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def reply_shared_details_saved(self, chat_id: int) -> None:
        self.bot.send_message(chat_id=chat_id,
                              text=f'Thank You! &#128525; for your benevolence. {Constants.LOCATION_SAVED}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def no_share_found(self, chat_id: int) -> None:
        self.bot.send_message(chat_id=chat_id,
                              text=f'Sorry! &#57608; {Constants.NO_SHARE}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def reply_nearby_shares(self, chat_id: int, shares: Iterable[Dict[str, Any]]) -> None:
        message: str = f'{Constants.FOUND_SHARE_PREFIX}\n\n'

        for share in shares:
            message += f'@{share["username"]}\n'

        message += f'\n{Constants.FOUND_SHARE_SUFFIX}'

        self.bot.send_message(chat_id=chat_id,
                              text=message,
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)

    def reply_server_error(self, chat_id: int) -> None:
        self.bot.send_message(chat_id=chat_id,
                              text=f'Sorry! &#57608; {Constants.SERVER_ERROR}',
                              reply_markup=ReplyKeyboardRemove(),
                              parse_mode=ParseMode.HTML)
