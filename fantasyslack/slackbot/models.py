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

    # @property
    # def user(self):
    #     return self.user

    @property
    def user(self):
        return self._data.get('user', None)

    @property
    def text(self):
        return self._data.get('text', None)

    @property
    def subtype(self):
        return self._data.get('subtype', None)

    @property
    def datetime(self):
        return datetime.fromtimestamp(float(self._data['ts']))

    @property
    def user_obj__real_name(self):
        if self.user:
            return self.user_obj.real_name
        else:
            return None

    def __str__(self):
        return 'SlackMessage: {self.object_id}, {self.user}, {self.datetime}'.format(**locals())


class SlackUser(SlackObject):
    def __init__(self, data):
        self._data = data

    @property
    def real_name(self):
        return self._data['profile'].get('real_name', None)
