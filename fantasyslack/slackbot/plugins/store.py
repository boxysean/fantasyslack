import logging
from pprint import pformat

from fantasyslack import settings
from fantasyslack.slackbot.mongo import MongoDAO

crontable = []
outputs = []

blacklist_types = ['pong']


def catch_all(data):
    if data['type'] not in blacklist_types:
        mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
        mongo_dao.store_message(data)
