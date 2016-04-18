import logging
from pprint import pformat

from fantasyslack import settings
from fantasyslack.utils.mongo import MongoDAO

crontable = []
outputs = []


def process_message(data):

    logging.info(pformat(data))

    mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
    mongo_dao.store_message(data)
