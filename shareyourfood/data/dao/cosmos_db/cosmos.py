import os
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

    def save_entry(self, entry: Entry) -> None:
        entry.id = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.url))
        self.container.upsert_item(entry.to_dict())

    def find_food(self, latitude: float, longitude: float) -> None:
        query: str = CosmosQuery.find_nearby_food(latitude=latitude,
                                                  longitude=longitude)
        self.container.query_items(query=query,
                                   enable_cross_partition_query=True)

    def find_entry(self, chat_id: int, username: str, message_id: int):
        query: str = CosmosQuery.find_nearby_entry(chat_id=chat_id,
                                                   username=username,
                                                   message_id=message_id)
        self.container.query_items(query=query,
                                   enable_cross_partition_query=True)
