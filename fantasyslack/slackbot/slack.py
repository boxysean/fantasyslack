from slackclient import SlackClient

class SlackDAO(object):
    def __init__(self, token):
        self.client = SlackClient(token)

    def get_user_list(self):
        res = self.client.api_call('users.list')
        return res['members']
