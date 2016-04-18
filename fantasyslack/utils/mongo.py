from pymongo import MongoClient

from fantasyslack import settings

class MongoDAO(object):
    def __init__(self, mongo_host, database_name, mongo_port=settings.MONGO_PORT):
        self.client = MongoClient(mongo_host, mongo_port)
        self.database = self.client[database_name]

    def store_message(self, message_data):
        collection = self.database['messages']
        collection.insert_one(message_data)
