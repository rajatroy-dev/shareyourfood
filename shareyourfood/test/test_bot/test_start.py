import json
import unittest
from unittest.mock import Mock, PropertyMock, patch

import azure.functions as func

from shareyourfood.bot.start import Start


class Test_Start(unittest.TestCase):
    token: str
    chat_id: int
    username: str
    full_name: str
    message_id: int
    latitude: float
    longitude: float
    start: str
    share: str
    request: str
    req: func.HttpRequest

    @classmethod
    def setUpClass(cls) -> None:
        cls.token = 'token'
        cls.chat_id = 123
        cls.username = 'username'
        cls.full_name = 'full_name'
        cls.message_id = 123
        cls.latitude = 11.11
        cls.longitude = 12.12
        cls.start = '/start'
        cls.share = '/share'
        cls.request = '/request'
        cls.req = func.HttpRequest(
            method='POST',
            body=json.dumps({'name': 'Test'}).encode('utf8'),
            url='/api/HttpTrigger',
            params=None)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.token = None
        cls.chat_id = None
        cls.username = None
        cls.full_name = None
        cls.message_id = None
        cls.latitude = None
        cls.longitude = None
        cls.start = None
        cls.share = None
        cls.request = None
        cls.req = None
        return super().tearDownClass()

    @patch('shareyourfood.bot.start.os.getenv', autospec=True)
    @patch('shareyourfood.bot.start.Bot', autospec=True)
    @patch('shareyourfood.bot.start.Update', autospec=True)
    @patch('shareyourfood.bot.start.Handle', autospec=True)
    def test_chat_start(cls, Handle, Update, Bot, os_getenv):
        os_getenv.return_value = cls.token
        Update.de_json.return_value = Mock(
            effective_chat=PropertyMock(
                id=cls.chat_id,
                username=cls.username,
                full_name=cls.full_name,
            ),
            effective_message=PropertyMock(
                message_id=cls.message_id,
                text=cls.start
            )
        )
        start = Start(cls.req)
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        Handle.assert_called_once()
        instance = Handle.return_value
        start.chat()
        assert instance.introduction.call_count == 1
        assert instance.share.call_count == 0
        assert instance.request.call_count == 0
        assert instance.location.call_count == 0
        instance.introduction.assert_called_once_with(
            cls.chat_id, cls.full_name)

    @patch('shareyourfood.bot.start.os.getenv', autospec=True)
    @patch('shareyourfood.bot.start.Bot', autospec=True)
    @patch('shareyourfood.bot.start.Update', autospec=True)
    @patch('shareyourfood.bot.start.Handle', autospec=True)
    def test_chat_share(cls, Handle, Update, Bot, os_getenv):
        os_getenv.return_value = cls.token
        Update.de_json.return_value = Mock(
            effective_chat=PropertyMock(
                id=cls.chat_id,
                username=cls.username,
                full_name=cls.full_name,
            ),
            effective_message=PropertyMock(
                message_id=cls.message_id,
                text=cls.share
            )
        )
        start = Start(cls.req)
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        Handle.assert_called_once()
        instance = Handle.return_value
        start.chat()
        assert instance.introduction.call_count == 0
        assert instance.share.call_count == 1
        assert instance.request.call_count == 0
        assert instance.location.call_count == 0
        instance.share.assert_called_once_with(
            cls.chat_id, cls.username, cls.message_id)

    @patch('shareyourfood.bot.start.os.getenv', autospec=True)
    @patch('shareyourfood.bot.start.Bot', autospec=True)
    @patch('shareyourfood.bot.start.Update', autospec=True)
    @patch('shareyourfood.bot.start.Handle', autospec=True)
    def test_chat_request(cls, Handle, Update, Bot, os_getenv):
        os_getenv.return_value = cls.token
        Update.de_json.return_value = Mock(
            effective_chat=PropertyMock(
                id=cls.chat_id,
                username=cls.username,
                full_name=cls.full_name,
            ),
            effective_message=PropertyMock(
                message_id=cls.message_id,
                text=cls.request
            )
        )
        start = Start(cls.req)
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        Handle.assert_called_once()
        instance = Handle.return_value
        start.chat()
        assert instance.introduction.call_count == 0
        assert instance.share.call_count == 0
        assert instance.request.call_count == 1
        assert instance.location.call_count == 0
        instance.request.assert_called_once_with(
            cls.chat_id, cls.username, cls.message_id)

    @patch('shareyourfood.bot.start.os.getenv', autospec=True)
    @patch('shareyourfood.bot.start.Bot', autospec=True)
    @patch('shareyourfood.bot.start.Update', autospec=True)
    @patch('shareyourfood.bot.start.Handle', autospec=True)
    def test_chat_location(cls, Handle, Update, Bot, os_getenv):
        os_getenv.return_value = cls.token
        Update.de_json.return_value = Mock(
            effective_chat=PropertyMock(
                id=cls.chat_id,
                username=cls.username,
                full_name=cls.full_name,
            ),
            effective_message=PropertyMock(
                message_id=cls.message_id,
                text=None,
                location=PropertyMock(
                    latitude=cls.latitude,
                    longitude=cls.longitude
                )
            )
        )
        start = Start(cls.req)
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        Handle.assert_called_once()
        instance = Handle.return_value
        start.chat()
        assert instance.introduction.call_count == 0
        assert instance.share.call_count == 0
        assert instance.request.call_count == 0
        assert instance.location.call_count == 1
        instance.location.assert_called_once_with(
            cls.chat_id, cls.username, cls.message_id, cls.latitude, cls.longitude)

    @patch('shareyourfood.bot.start.os.getenv', autospec=True)
    @patch('shareyourfood.bot.start.Bot', autospec=True)
    @patch('shareyourfood.bot.start.Update', autospec=True)
    @patch('shareyourfood.bot.start.Handle', autospec=True)
    def test_chat_unknown_text(cls, Handle, Update, Bot, os_getenv):
        os_getenv.return_value = cls.token
        Update.de_json.return_value = Mock(
            effective_chat=PropertyMock(
                id=cls.chat_id,
                username=cls.username,
                full_name=cls.full_name,
            ),
            effective_message=PropertyMock(
                message_id=cls.message_id,
                text='sdfasdad',
                location=None
            )
        )
        start = Start(cls.req)
        os_getenv.assert_called_once_with('TOKEN')
        Bot.assert_called_once_with(cls.token)
        Handle.assert_called_once()
        instance = Handle.return_value
        start.chat()
        assert instance.introduction.call_count == 1
        assert instance.share.call_count == 0
        assert instance.request.call_count == 0
        assert instance.location.call_count == 0
        instance.introduction.assert_called_once_with(
            cls.chat_id, cls.full_name)


if __name__ == '__main__':
    unittest.main()
