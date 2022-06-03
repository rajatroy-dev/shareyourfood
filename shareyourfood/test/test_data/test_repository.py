from typing import Any, Dict, Iterable
import unittest
from unittest.mock import patch

from shareyourfood.data.repository import Repository


class Test_Repository(unittest.TestCase):
    chat_id: int
    message_id: int
    full_name: str
    username: str
    latitude: str
    longitude: str
    shares: Iterable[Dict[str, Any]]

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

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_save_share_food_details_dao_false(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.save_entry.return_value = False
        repository = Repository()
        response = repository\
            .save_share_food_details(cls.chat_id, cls.username, cls.message_id, cls.latitude, cls.longitude)
        assert Dao.call_count == 1
        assert Dao_instance.save_entry.call_count == 1
        assert response == False

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_save_share_food_details_dao_true(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.save_entry.return_value = True
        repository = Repository()
        response = repository\
            .save_share_food_details(cls.chat_id, cls.username, cls.message_id, cls.latitude, cls.longitude)
        assert Dao.call_count == 1
        assert Dao_instance.save_entry.call_count == 1
        assert response == True

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_save_request_food_details_dao_false(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.save_entry.return_value = False
        repository = Repository()
        response = repository\
            .save_request_food_details(cls.chat_id, cls.username, cls.message_id)
        assert Dao.call_count == 1
        assert Dao_instance.save_entry.call_count == 1
        assert response == False

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_save_request_food_details_dao_true(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.save_entry.return_value = True
        repository = Repository()
        response = repository\
            .save_request_food_details(cls.chat_id, cls.username, cls.message_id)
        assert Dao.call_count == 1
        assert Dao_instance.save_entry.call_count == 1
        assert response == True

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_find_entry(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.find_entry.return_value = cls.shares
        repository = Repository()
        response = repository\
            .find_entry(cls.chat_id, cls.username, cls.message_id)
        assert Dao.call_count == 1
        assert Dao_instance.find_entry.call_count == 1
        assert response == cls.shares
        Dao_instance.find_entry\
            .assert_called_once_with(cls.chat_id, cls.username, cls.message_id)

    @patch('shareyourfood.data.repository.Dao', autospec=True)
    def test_find_food(cls, Dao):
        Dao_instance = Dao.return_value
        Dao_instance.find_food.return_value = cls.shares
        repository = Repository()
        response = repository\
            .find_food(cls.latitude, cls.longitude)
        assert Dao.call_count == 1
        assert Dao_instance.find_food.call_count == 1
        assert response == cls.shares
        Dao_instance.find_food\
            .assert_called_once_with(cls.latitude, cls.longitude)
