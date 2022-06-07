from typing import Any, Dict, Iterable
import unittest
from unittest.mock import patch
from telegram import KeyboardButton, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove

from shareyourfood.bot.constants import Constants
from shareyourfood.bot.conversation import Conversation


class Test_Conversation(unittest.TestCase):
    token: str
    chat_id: int
    full_name: str
    shares: Iterable[Dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.token = 'token'
        cls.chat_id = 123
        cls.full_name = 'full_name'
        cls.shares = [
            {'username': 'dasd342'},
            {'username': 'erter76'},
            {'username': 'jtutgrh'}
        ]
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.token = None
        cls.chat_id = None
        cls.full_name = None
        cls.shares = None
        return super().tearDownClass()

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_introduce(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.introduce(cls.chat_id, cls.full_name)
        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=f'Hi! <b>{cls.full_name}</b> &#128075;, {Constants.INTRODUCTION}',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_ask_location_for_share(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.ask_location_for_share(cls.chat_id)

        location_keyboard: KeyboardButton = KeyboardButton(
            text='Share location', request_location=True)
        custom_keyboard: list[list[KeyboardButton]] = [[location_keyboard]]
        reply_markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=Constants.SHARE_LOCATION,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_ask_location_for_request(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.ask_location_for_request(cls.chat_id)

        location_keyboard: KeyboardButton = KeyboardButton(
            text='Share location', request_location=True)
        custom_keyboard: list[list[KeyboardButton]] = [[location_keyboard]]
        reply_markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            custom_keyboard, resize_keyboard=True)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=Constants.REQUEST_LOCATION,
            reply_markup=reply_markup
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_unknown_location(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.unknown_location(cls.chat_id)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=f'Sorry! &#128531; {Constants.UNKOWN_LOCATION}',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_reply_shared_details_saved(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.reply_shared_details_saved(cls.chat_id)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=f'Thank You! &#128525; for your benevolence. {Constants.LOCATION_SAVED}',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_no_share_found(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.no_share_found(cls.chat_id)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=f'Sorry! &#128531; {Constants.NO_SHARE}',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_reply_nearby_shares(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        message: str = f'{Constants.FOUND_SHARE_PREFIX}\n\n'
        for share in cls.shares:
            message += f'@{share["username"]}\n'
        message += f'\n{Constants.FOUND_SHARE_SUFFIX}'
        conversation.reply_nearby_shares(cls.chat_id, cls.shares)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=message,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )

    @patch('shareyourfood.bot.conversation.os.getenv', autospec=True)
    @patch('shareyourfood.bot.conversation.Bot', autospec=True)
    def test_reply_server_error(cls, Bot, os_getenv):
        os_getenv.return_value = cls.token
        conversation = Conversation()
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        instance = Bot.return_value
        conversation.reply_server_error(cls.chat_id)

        assert instance.send_message.call_count == 1
        instance.send_message.assert_called_once_with(
            chat_id=cls.chat_id,
            text=f'Sorry! &#128531; {Constants.SERVER_ERROR}',
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML
        )
