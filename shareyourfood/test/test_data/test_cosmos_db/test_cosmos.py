from azure.cosmos import exceptions
from typing import Any, Iterable
import unittest
from unittest.mock import Mock, patch

from shareyourfood.data.dao.cosmos_db.cosmos import Cosmos
from shareyourfood.data.model.entry import Entry
from shareyourfood.data.model.location import PointLocation


class Test_Cosmos(unittest.TestCase):
    chat_id: int
    message_id: int
    username: str
    latitude: str
    longitude: str

    @classmethod
    def setUpClass(cls) -> None:
        cls.chat_id = 123
        cls.message_id = 123
        cls.username = 'username'
        cls.latitude = 11.11
        cls.longitude = 12.12
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.chat_id = None
        cls.message_id = None
        cls.username = None
        cls.latitude = None
        cls.longitude = None
        return super().tearDownClass()

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_init_no_exception(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        Cosmos()
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_init_with_first_exception(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value

        create_database_instance_exception = CosmosClient_instance.create_database
        create_database_instance_exception.side_effect = Mock(
            side_effect=exceptions.CosmosResourceExistsError(404))

        get_database_instance = CosmosClient_instance.get_database_client.return_value

        Cosmos()

        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert CosmosClient_instance.get_database_client.call_count == 1
        assert get_database_instance.create_container.call_count == 1
        assert get_database_instance.get_container_client.call_count == 0

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_init_with_second_exception(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value

        create_container_instance_exception = create_database_instance.create_container
        create_container_instance_exception.side_effect = Mock(
            side_effect=exceptions.CosmosResourceExistsError(404))

        Cosmos()

        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert CosmosClient_instance.get_database_client.call_count == 0
        assert create_database_instance.create_container.call_count == 1
        assert create_database_instance.get_container_client.call_count == 1

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_init_with_all_exception(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        get_database_instance = CosmosClient_instance.get_database_client.return_value

        create_database_instance_exception = CosmosClient_instance.create_database
        create_database_instance_exception.side_effect = Mock(
            side_effect=exceptions.CosmosResourceExistsError(404))
        create_container_instance_exception = get_database_instance.create_container
        create_container_instance_exception.side_effect = Mock(
            side_effect=exceptions.CosmosResourceExistsError(404))

        Cosmos()

        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert CosmosClient_instance.get_database_client.call_count == 1
        assert get_database_instance.create_container.call_count == 1
        assert get_database_instance.get_container_client.call_count == 1

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.uuid', autospec=True)
    def test_save_entry_fail(cls, uuid, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        entry = Entry(id='', message_type='request', entry_id='', chat_id=cls.chat_id, username=cls.username,
                      message_id=cls.message_id, location=PointLocation([cls.latitude, cls.longitude]))
        create_container_instance.upsert_item.return_value = None
        response = cosmos.save_entry(entry)
        assert uuid.uuid5.call_count == 1
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.upsert_item.call_count == 1
        assert response == False

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.uuid', autospec=True)
    def test_save_entry_fail_no_id(cls, uuid, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        entry = Entry(id='', message_type='request', entry_id='', chat_id=cls.chat_id, username=cls.username,
                      message_id=cls.message_id, location=PointLocation([cls.latitude, cls.longitude]))
        create_container_instance.upsert_item.return_value = {'entry': 'entry'}
        response = cosmos.save_entry(entry)
        assert uuid.uuid5.call_count == 1
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.upsert_item.call_count == 1
        assert response == False

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.uuid', autospec=True)
    def test_save_entry_success(cls, uuid, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        entry = Entry(id='', message_type='request', entry_id='', chat_id=cls.chat_id, username=cls.username,
                      message_id=cls.message_id, location=PointLocation([cls.latitude, cls.longitude]))
        create_container_instance.upsert_item.return_value = {'id': 'id'}
        response = cosmos.save_entry(entry)
        assert uuid.uuid5.call_count == 1
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.upsert_item.call_count == 1
        assert response == True

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_entry_fail_empty_response(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items.return_value = []
        response = cosmos.find_entry(cls.chat_id, cls.username, cls.message_id)
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response == None

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_entry_fail_no_response(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items.return_value = None
        response = cosmos.find_entry(cls.chat_id, cls.username, cls.message_id)
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response == None

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_entry_fail_multi_len_response(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items\
            .return_value = [{'id': 'id'}, {'id': 'id'}]
        response = cosmos.find_entry(cls.chat_id, cls.username, cls.message_id)
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response == None

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_entry_success(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items\
            .return_value = [{'id': 'id'}]
        response = cosmos.find_entry(cls.chat_id, cls.username, cls.message_id)
        assert os_getenv.call_count == 5
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response.get('id') == 'id'

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_food_fail_no_response(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items.return_value = None
        response = cosmos.find_food(cls.latitude, cls.longitude)
        print(os_getenv.call_count)
        assert os_getenv.call_count == 6  # 1 more inside query
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response == None

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_food_fail_empty_response(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items.return_value = []
        response = cosmos.find_food(cls.latitude, cls.longitude)
        print(os_getenv.call_count)
        assert os_getenv.call_count == 6  # 1 more inside query
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response == None

    @patch('shareyourfood.data.dao.cosmos_db.cosmos.os.getenv', autospec=True)
    @patch('shareyourfood.data.dao.cosmos_db.cosmos.CosmosClient', autospec=True)
    def test_find_food_success(cls, CosmosClient, os_getenv):
        CosmosClient_instance = CosmosClient.return_value
        create_database_instance = CosmosClient_instance.create_database.return_value
        create_container_instance = create_database_instance.create_container.return_value
        cosmos = Cosmos()
        create_container_instance.query_items\
            .return_value = [{'id': 'id'}]
        response = cosmos.find_food(cls.latitude, cls.longitude)
        print(os_getenv.call_count)
        assert os_getenv.call_count == 6  # 1 more inside query
        assert CosmosClient.call_count == 1
        assert CosmosClient_instance.create_database.call_count == 1
        assert create_database_instance.create_container.call_count == 1
        assert create_container_instance.query_items.call_count == 1
        assert response[0].get('id') == 'id'
