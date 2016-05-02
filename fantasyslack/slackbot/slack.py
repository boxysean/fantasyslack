from slackclient import SlackClient

class SlackDAO(object):
    def __init__(self, token):
        self.client = SlackClient(token)

    def get_user_list(self):
        res = self.client.api_call('users.list')
        return res['members']

    def get_im_channel_by_user_id(self, user_id):
        res = self.client.api_call('im.list')

        for im in res['ims']:
            if im['user'] == user_id:
                return im['id']

        return None

    def post_message(self, channel, message):
        self.client.api_call('chat.postMessage', channel=channel, text=message)
