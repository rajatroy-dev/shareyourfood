import os
from typing import Any, Iterable
import uuid
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from shareyourfood.data.dao.cosmos_db.query import CosmosQuery

from shareyourfood.data.model.entry import Entry


class Cosmos:
    def __init__(self) -> None:
        self.url = os.getenv('ACCOUNT_URI')
        self.key = os.getenv('ACCOUNT_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = os.getenv('DATABASE')
        self.container_name = os.getenv('CONTAINER')
        self.url = os.getenv('URL_FOR_UUID')

        try:
            self.database = self.client.create_database(self.database_name)
        except exceptions.CosmosResourceExistsError:
            self.database = self.client.get_database_client(self.database_name)

        try:
            self.container = self.database.create_container(
                id=self.container_name, partition_key=PartitionKey(path='/message_type'))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(
                self.container_name)
        except exceptions.CosmosHttpResponseError:
            raise

    def save_entry(self, entry: Entry) -> bool:
        entry.id = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.url))
        entry.entry_id = entry.id
        response: dict[str, Any] = self.container.upsert_item(entry.to_dict())

        if response \
                and response.get('id') is not None:
            return True
        return False

    def find_entry(self, chat_id: int, username: str, message_id: int) -> dict[str, Any]:
        query: str = CosmosQuery.find_nearby_entry(chat_id=chat_id,
                                                   username=username,
                                                   message_id=message_id)
        response: Iterable[dict[str, Any]] = self.container.query_items(query=query,
                                                                        enable_cross_partition_query=True)

        if not response:
            return None
        elif len(response) == 0:
            return None
        elif len(response) > 1:
            return None
        return response[0]

    def find_food(self, latitude: float, longitude: float) -> Iterable[dict[str, Any]]:
        query: str = CosmosQuery.find_nearby_food(latitude=latitude,
                                                  longitude=longitude)
        response: Iterable[dict[str, Any]] = self.container.query_items(query=query,
                                                                        enable_cross_partition_query=True)

        if not response:
            return None
        elif len(response) == 0:
            return None
        return response[0]
