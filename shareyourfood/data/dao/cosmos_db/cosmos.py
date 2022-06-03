import os
from typing import Any, Dict, Iterable, List
import uuid
from azure.cosmos import CosmosClient, PartitionKey, exceptions, DatabaseProxy, ContainerProxy
from shareyourfood.data.dao.cosmos_db.query import CosmosQuery

from shareyourfood.data.model.entry import Entry


class Cosmos:
    def __init__(self) -> None:
        self.url: str = os.getenv('ACCOUNT_URI')
        self.key: str = os.getenv('ACCOUNT_KEY')
        self.client: CosmosClient = CosmosClient(self.url, credential=self.key)
        self.database_name: str = os.getenv('DATABASE')
        self.container_name: str = os.getenv('CONTAINER')
        self.url_for_uuid: str = os.getenv('URL_FOR_UUID')

        try:
            self.database: DatabaseProxy = self.client.create_database(self.database_name)
        except exceptions.CosmosResourceExistsError:
            self.database: DatabaseProxy = self.client.get_database_client(self.database_name)

        try:
            self.container: ContainerProxy = self.database.create_container(
                id=self.container_name, partition_key=PartitionKey(path='/message_type'))
        except exceptions.CosmosResourceExistsError:
            self.container: ContainerProxy = self.database.get_container_client(
                self.container_name)
        except exceptions.CosmosHttpResponseError:
            raise

    def save_entry(self, entry: Entry) -> bool:
        entry.id = str(uuid.uuid5(uuid.NAMESPACE_URL, self.url_for_uuid))
        entry.entry_id = entry.id
        response: Dict[str, Any] = self.container.upsert_item(entry.to_dict())

        if response \
                and response.get('id') is not None:
            return True
        return False

    def find_entry(self, chat_id: int, username: str, message_id: int) -> Dict[str, Any]:
        query: str = CosmosQuery.find_nearby_entry(chat_id=chat_id,
                                                   username=username,
                                                   message_id=message_id)
        response: Iterable[Dict[str, Any]] = self.container.query_items(query=query,
                                                                        enable_cross_partition_query=True)
        response_len_count: int = 0
        response_item: Dict[str, Any]
        if response:
            for item in response:
                response_len_count += 1
                response_item = item
            if response_len_count == 1:
                return response_item
        return None

    def find_food(self, latitude: float, longitude: float) -> Iterable[Dict[str, Any]]:
        query: str = CosmosQuery.find_nearby_food(latitude=latitude,
                                                  longitude=longitude)
        response: Iterable[Dict[str, Any]] = self.container.query_items(query=query,
                                                                        enable_cross_partition_query=True)
        response_items: List[Dict[str, Any]] = []
        if response:
            for item in response:
                response_items.append(item)
            return response_items
        return None
