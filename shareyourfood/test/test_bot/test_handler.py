from typing import Any, Iterable
import unittest
from unittest.mock import patch
from shareyourfood.bot.constants import Constants

from shareyourfood.bot.handler import Handle


class Test_Handler(unittest.TestCase):
    chat_id: int
    message_id: int
    full_name: str
    username: str
    latitude: str
    longitude: str
    shares: Iterable[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.chat_id = 123
        cls.message_id = 123
        cls.full_name = 'full_name'
        cls.username = 'username'
        cls.latitude = 11.11
        cls.longitude = 12.12
        cls.shares = [
            {'username': 'dasd342'},
            {'username': 'erter76'},
            {'username': 'jtutgrh'}
        ]
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.chat_id = None
        cls.message_id = None
        cls.full_name = None
        cls.username = None
        cls.latitude = None
        cls.longitude = None
        cls.shares = None
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
        Converstion_instance.ask_location_for_share\
            .assert_called_once_with(cls.chat_id)

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
        Converstion_instance.reply_server_error\
            .assert_called_once_with(cls.chat_id)

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
        Converstion_instance.ask_location_for_request\
            .assert_called_once_with(cls.chat_id)

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
        Converstion_instance.reply_server_error\
            .assert_called_once_with(cls.chat_id)

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_location_repository_return_none(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.find_entry.return_value = {}
        handle = Handle()
        handle.location(cls.chat_id, cls.username,
                        cls.message_id, cls.latitude, cls.longitude)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.find_entry.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 0
        assert Converstion_instance.reply_shared_details_saved.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 0
        assert Repository_instance.find_food.call_count == 0
        assert Converstion_instance.reply_nearby_shares.call_count == 0
        assert Converstion_instance.no_share_found.call_count == 0
        assert Converstion_instance.unknown_location.call_count == 1
        Repository_instance.find_entry.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id - 2
        )
        Converstion_instance.unknown_location\
            .assert_called_once_with(cls.chat_id)

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_location_repository_return_share_repository_return_false(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.find_entry\
            .return_value = {'message_type': Constants.SHARE}
        Repository_instance.save_share_food_details.return_value = False
        handle = Handle()
        handle.location(cls.chat_id, cls.username,
                        cls.message_id, cls.latitude, cls.longitude)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.find_entry.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 1
        assert Converstion_instance.reply_shared_details_saved.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 1
        assert Repository_instance.find_food.call_count == 0
        assert Converstion_instance.reply_nearby_shares.call_count == 0
        assert Converstion_instance.no_share_found.call_count == 0
        assert Converstion_instance.unknown_location.call_count == 0
        Repository_instance.find_entry.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id - 2
        )
        Repository_instance.save_share_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id,
            latitude=cls.latitude,
            longitude=cls.longitude
        )
        Converstion_instance.reply_server_error\
            .assert_called_once_with(cls.chat_id)

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_location_repository_return_share_repository_return_true(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.find_entry\
            .return_value = {'message_type': Constants.SHARE}
        Repository_instance.save_share_food_details.return_value = True
        handle = Handle()
        handle.location(cls.chat_id, cls.username,
                        cls.message_id, cls.latitude, cls.longitude)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.find_entry.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 1
        assert Converstion_instance.reply_shared_details_saved.call_count == 1
        assert Converstion_instance.reply_server_error.call_count == 0
        assert Repository_instance.find_food.call_count == 0
        assert Converstion_instance.reply_nearby_shares.call_count == 0
        assert Converstion_instance.no_share_found.call_count == 0
        assert Converstion_instance.unknown_location.call_count == 0
        Repository_instance.find_entry.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id - 2
        )
        Repository_instance.save_share_food_details.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id,
            latitude=cls.latitude,
            longitude=cls.longitude
        )
        Converstion_instance.reply_shared_details_saved\
            .assert_called_once_with(cls.chat_id)

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_location_repository_return_request_repository_return_none(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.find_entry\
            .return_value = {'message_type': Constants.REQUEST}
        Repository_instance.find_food.return_value = None
        handle = Handle()
        handle.location(cls.chat_id, cls.username,
                        cls.message_id, cls.latitude, cls.longitude)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.find_entry.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 0
        assert Converstion_instance.reply_shared_details_saved.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 0
        assert Repository_instance.find_food.call_count == 1
        assert Converstion_instance.reply_nearby_shares.call_count == 0
        assert Converstion_instance.no_share_found.call_count == 1
        assert Converstion_instance.unknown_location.call_count == 0
        Repository_instance.find_entry.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id - 2
        )
        Repository_instance.find_food.assert_called_once_with(
            latitude=cls.latitude,
            longitude=cls.longitude
        )
        Converstion_instance.no_share_found\
            .assert_called_once_with(cls.chat_id)

    @patch('shareyourfood.bot.handler.Conversation', autospec=True)
    @patch('shareyourfood.bot.handler.Repository', autospec=True)
    def test_location_repository_return_request_repository_return_true(cls, Repository, Conversation):
        Converstion_instance = Conversation.return_value
        Repository_instance = Repository.return_value
        Repository_instance.find_entry\
            .return_value = {'message_type': Constants.REQUEST}
        Repository_instance.find_food.return_value = cls.shares
        handle = Handle()
        handle.location(cls.chat_id, cls.username,
                        cls.message_id, cls.latitude, cls.longitude)
        assert Repository.call_count == 1
        assert Conversation.call_count == 1
        assert Repository_instance.find_entry.call_count == 1
        assert Repository_instance.save_share_food_details.call_count == 0
        assert Converstion_instance.reply_shared_details_saved.call_count == 0
        assert Converstion_instance.reply_server_error.call_count == 0
        assert Repository_instance.find_food.call_count == 1
        assert Converstion_instance.reply_nearby_shares.call_count == 1
        assert Converstion_instance.no_share_found.call_count == 0
        assert Converstion_instance.unknown_location.call_count == 0
        Repository_instance.find_entry.assert_called_once_with(
            chat_id=cls.chat_id,
            username=cls.username,
            message_id=cls.message_id - 2
        )
        Repository_instance.find_food.assert_called_once_with(
            latitude=cls.latitude,
            longitude=cls.longitude
        )
        Converstion_instance.reply_nearby_shares\
            .assert_called_once_with(cls.chat_id, cls.shares)
