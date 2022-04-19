import unittest
from unittest.mock import patch

from shareyourfood.bot.handler import Handle


class Test_Handler(unittest.TestCase):
    chat_id: int
    message_id: int
    full_name: str
    username: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.chat_id = 123
        cls.message_id = 123
        cls.full_name = 'full_name'
        cls.username = 'username'
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.chat_id = None
        cls.message_id = None
        cls.full_name = None
        cls.username = None
        return super().tearDownClass()

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_introduction(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        handle = Handle()
        handle.introduction(cls.chat_id, cls.full_name)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Converstion_instance.introduce.call_count == 1
        Converstion_instance.introduce.assert_called_once_with(
            chat_id=cls.chat_id,
            full_name=cls.full_name
        )

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_share_repository_return_true(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.save_share_food_details.return_value = True
        handle = Handle()
        handle.share(cls.chat_id, cls.username, cls.message_id)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 1
        assert Converstion_instance.ask_location_for_share.call_count == 1
        assert Converstion_instance.reply_server_error.call_count == 0
        Repository_instance.save_share_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id
        )
        Converstion_instance.ask_location_for_share.assert_called_once_with(
            chat_id=cls.chat_id
        )

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_share_repository_return_false(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.save_share_food_details.return_value = False
        handle = Handle()
        handle.share(cls.chat_id, cls.username, cls.message_id)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 1
        assert Converstion_instance.ask_location_for_share.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 1
        Repository_instance.save_share_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id
        )
        Converstion_instance.reply_server_error.assert_called_once_with(
            chat_id=cls.chat_id
        )

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_request_repository_return_true(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.save_request_food_details.return_value = True
        handle = Handle()
        handle.request(cls.chat_id, cls.username, cls.message_id)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.save_request_food_details.call_count == 1
        assert Converstion_instance.ask_location_for_request.call_count == 1
        assert Converstion_instance.reply_server_error.call_count == 0
        Repository_instance.save_request_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id
        )
        Converstion_instance.ask_location_for_request.assert_called_once_with(
            chat_id=cls.chat_id
        )

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_request_repository_return_false(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.save_request_food_details.return_value = False
        handle = Handle()
        handle.request(cls.chat_id, cls.username, cls.message_id)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.save_request_food_details.call_count == 1
        assert Converstion_instance.ask_location_for_request.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 1
        Repository_instance.save_request_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id
        )
        Converstion_instance.reply_server_error.assert_called_once_with(
            chat_id=cls.chat_id
        )
