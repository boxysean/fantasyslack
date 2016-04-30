import logging
import re


class FantasySlackStat(object):
    def __init__(self):
        pass

    def compute(self, messages, users):
        raise NotImplementedError()


class StatReactions(FantasySlackStat):
    name = 'Reactions Gained'

    def __init__(self, slack_message_factory):
        super(StatReactions, self).__init__()
        self.slack_message_factory = slack_message_factory

    def compute(self, messages, users):
        res = {user.real_name: 0 for user in users}

        for message in messages:
            if message.type == 'reaction_added':
                msgs = self.slack_message_factory.get(filter_dict={'ts': message._data['item']['ts']})
                if not msgs:
                    logging.warning('skipping message because it is unavailable')
                    continue
                original_message = msgs[0]
                key = original_message.user_obj__real_name
                res[key] = res.get(key, 0) + 1

        return res


class StatChattyKathy(FantasySlackStat):
    name = 'Chatty Kathy'

    def __init__(self, slack_message_factory):
        super(StatChattyKathy, self).__init__()
        self.slack_message_factory = slack_message_factory

    def compute(self, messages, users):
        res = {user.real_name: 0 for user in users}

        for message in messages:
            if message.type == 'message' and message.subtype != 'message_changed':
                key = message.user_obj__real_name
                res[key] = res.get(key, 0) + 1

        return res


class StatEmojiMaster(FantasySlackStat):
    name = 'Emoji Master'

    def __init__(self, slack_message_factory):
        super(StatEmojiMaster, self).__init__()
        self.slack_message_factory = slack_message_factory

    def compute(self, messages, users):
        res = {user.real_name: 0 for user in users}

        for message in messages:
            if message.type == 'message' and message.subtype != 'message_changed':
                emojis = len(re.split(r':[^ ]+:', message.text)) - 1
                key = message.user_obj__real_name
                res[key] = res.get(key, 0) + emojis


        return res


class StatShouter(FantasySlackStat):
    name = 'Shouter'

    def __init__(self, slack_message_factory):
        super(StatShouter, self).__init__()
        self.slack_message_factory = slack_message_factory

    def compute(self, messages, users):
        res = {user.real_name: 0 for user in users}

        for message in messages:
            if message.type == 'message' and message.subtype != 'message_changed':
                if re.search(r'!!!', message.text) or message.text.upper() == message.text:
                    key = message.user_obj__real_name
                    res[key] = res.get(key, 0) + 1

        return res


class StatEditor(FantasySlackStat):
    name = 'Editor'

    def __init__(self, slack_message_factory):
        super(StatEditor, self).__init__()
        self.slack_message_factory = slack_message_factory

    def compute(self, messages, users):
        res = {user.real_name: 0 for user in users}

        for message in messages:
            if message.type == 'message' and message.subtype == 'message_changed':
                key = message.user_obj__real_name
                res[key] = res.get(key, 0) + 1

        return res
