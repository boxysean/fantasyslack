from fantasyslack import settings

from fantasyslack.slackbot.models import SlackMessage, SlackUser


class SlackFactory(object):
    def __init__(self, mongo_dao, slack_dao):
        self.mongo_dao = mongo_dao
        self.slack_dao = slack_dao


class SlackMessageFactory(SlackFactory):
    def __init__(self, mongo_dao, slack_dao):
        super(SlackMessageFactory, self).__init__(mongo_dao, slack_dao)

    def _attach_user(self, message):
        if not message.user:
            return

        user_data = self.mongo_dao.get_user_by_id(message.user)
        
        if not user_data:
            for datum in self.slack_dao.get_user_list():
                self.mongo_dao.store_user(datum)
                if message.subtype != 'message_changed' and datum['id'] == message.user:
                    user_data = datum
                elif message.subtype == 'message_changed' and datum['message']['id'] == message.user:
                    user_data = datum

        if user_data:
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


class SlackUserFactory(SlackFactory):
    def __init__(self, mongo_dao, slack_dao):
        super(SlackUserFactory, self).__init__(mongo_dao, slack_dao)

    def create_all(self):
        slack_users = []

        for user_datum in self.mongo_dao.get_users():
            slack_users.append(SlackUser(user_datum))

        return slack_users
