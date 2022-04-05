import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions


class Cosmos:
    def __init__(self) -> None:
        self.url = os.getenv('ACCOUNT_URI')
        self.key = os.getenv('ACCOUNT_KEY')
        self.client = CosmosClient(self.url, credential=self.key)
        self.database_name = os.getenv('DATABASE')
        self.container_name = os.getenv('CONTAINER')

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
