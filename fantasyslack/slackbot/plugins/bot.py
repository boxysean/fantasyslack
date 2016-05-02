from fantasyslack import settings
from fantasyslack.slackbot.bot import FantasySlackBot
from fantasyslack.slackbot.factory import SlackUserFactory
from fantasyslack.slackbot.mongo import MongoDAO
from fantasyslack.slackbot.slack import SlackDAO

crontable = []
outputs = []


def process_message(data):
    if data['channel'].startswith('D') and 'user' in data:
        mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
        slack_dao = SlackDAO(settings.SLACK_API_TOKEN)
        slack_user = SlackUserFactory(mongo_dao, slack_dao).create(data['user'])
        FantasySlackBot().process_direct_message(slack_user, data['text'])
