import os
from pymongo import MongoClient


class Mongo:
    def __init__(self) -> None:
        self.token = os.getenv('MongoDBConnectionString')
        self.client = MongoClient('mongodb://localhost:27017/')

    def __init__(self) -> None:
        pass

    def share_food(self):
        pass

    def request_food(self):
        pass
