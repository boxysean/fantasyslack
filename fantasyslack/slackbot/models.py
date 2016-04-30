from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from fantasyslack import settings


class SlackObject(object):
    pass


class SlackMessage(SlackObject):
    def __init__(self, data):
        self._data = data

    @property
    def object_id(self):
        return self._data.get('_id', None)

    @property
    def user(self):
        if self.type == 'user_change':
            return self._data['user']['id']  # turns out this message has rich user info
        elif self.type == 'message' and self._data.get('subtype') == 'message_changed':
            return self._data['message']['user']
        else:
            return self._data.get('user', None)

    @property
    def text(self):
        return self._data.get('text', None)

    @property
    def subtype(self):
        return self._data.get('subtype', None)

    @property
    def datetime(self):
        if 'ts' in self._data:
            return datetime.fromtimestamp(float(self._data['ts']))
        else:
            return None

    @property
    def type(self):
        return self._data.get('type', None)

    @property
    def user_obj__real_name(self):
        if self.user:
            return self.user_obj.real_name
        else:
            return None

    def __str__(self):
        return 'SlackMessage: {self.object_id}, {self.type}, {self.datetime}'.format(**locals())


class SlackUser(SlackObject):
    def __init__(self, data):
        self._data = data

    @property
    def real_name(self):
        return self._data['profile'].get('real_name', None)
