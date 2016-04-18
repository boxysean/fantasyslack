from fantasyslack import settings

from fantasyslack.slackbot.models import SlackMessage, SlackUser


class SlackMessageFactory(object):
    def __init__(self, mongo_dao, slack_dao):
        self.mongo_dao = mongo_dao
        self.slack_dao = slack_dao

    def _attach_user(self, message):
        if not message.user:
            return

        user_data = self.mongo_dao.get_user_by_id(message.user)

        if not user_data:
            for datum in self.slack_dao.get_user_list():
                self.mongo_dao.store_user(datum)
                if datum['id'] == message.user:
                    user_data = datum

        message.user_obj = SlackUser(user_data)

    def get(self, message_id=None, filter_dict={}):
        if message_id:
            slack_message_data = self.mongo_dao.get_message_by_id(message_id)
            slack_message = SlackMessage(slack_message_data)
            self._attach_user(slack_message)
            return slack_message
        else:
            slack_message_data = self.mongo_dao.get_messages(filter_dict)
            slack_messages = []

            for slack_message_datum in slack_message_data:
                slack_message = SlackMessage(slack_message_datum)
                self._attach_user(slack_message)
                slack_messages.append(slack_message)

            return slack_messages
