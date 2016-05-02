from pymongo import MongoClient
from bson.objectid import ObjectId

from fantasyslack import settings


class MongoDAO(object):
    def __init__(self, mongo_host, database_name, mongo_port=settings.MONGO_PORT):
        self.client = MongoClient(mongo_host, mongo_port)
        self.database = self.client[database_name]

    def store_message(self, message_data):
        collection = self.database['slackmessages']
        return collection.insert_one(message_data)

    def get_messages(self, filter_dict={}):
        collection = self.database['slackmessages']
        return collection.find(filter_dict)

    def get_message_by_id(self, message_id):
        collection = self.database['slackmessages']
        return collection.find_one({'_id': ObjectId(message_id)})

    def get_user_by_id(self, user_id):
        collection = self.database['slackusers']
        return collection.find_one({'id': user_id})

    def get_user_by_name(self, name):
        collection = self.database['slackusers']
        return collection.find_one({'name': name})

    def store_user(self, user_data):
        collection = self.database['slackusers']
        return collection.replace_one({'id': user_data['id']}, user_data, upsert=True)

    def get_users(self, filter_dict={}):
        collection = self.database['slackusers']
        return collection.find(filter_dict)
