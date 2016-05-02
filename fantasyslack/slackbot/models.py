from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from fantasyslack import settings
# from fantasyslack.slackbot.factory import SlackUserFactory
from fantasyslack.slackbot.mongo import MongoDAO
from fantasyslack.slackbot.slack import SlackDAO


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

    @property
    def id(self):
        return self._data['id']


class Game(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=256)
    slug = models.SlugField()
    channel = models.CharField(max_length=128)

    owner = models.ForeignKey('Player', related_name='games_owned')
    managers = models.ManyToManyField('Player', related_name='games_managed')

    draft_started_date = models.DateTimeField(null=True)
    draft_ended_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField()

    team_members = models.IntegerField()
    categories = models.ManyToManyField('Category')

    current_state = models.CharField(max_length=32)

    def has_started(self):
        return self.draft_ended_date is not None


class Team(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    owner = models.ForeignKey('Player', related_name='team_owner')
    players = models.ManyToManyField('Player')
    game = models.ForeignKey('Game')


class Player(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, null=True)
    slack_user_id = models.CharField(max_length=32)

    def __unicode__(self):
        return self.slack_user_id


class Transaction(models.Model):
    ADD = 'AD'
    DROP = 'DR'
    TRADE_FOR = 'TF'
    TRADE_TO = 'TT'

    ACTIONS = (
        (ADD, 'Add'),
        (DROP, 'Drop'),
        (TRADE_FOR, 'Trade For'),
        (TRADE_TO, 'Trade To'),
    )

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    action = models.CharField(choices=ACTIONS, max_length=16)


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    python_module_name = models.CharField(max_length=128)


class DraftOrder(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    team = models.ForeignKey(Team)
    game = models.ForeignKey(Game, db_index=True)
    order = models.IntegerField()


class Point(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    player = models.ForeignKey(Player)
    category = models.ForeignKey(Category)
    slack_timestamp = models.CharField(max_length=32)


class SlackBotUserDMState(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    player = models.ForeignKey(Player, db_index=True)
    state_class = models.CharField(max_length=64)


class SlackBotUserDMStateTable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    state = models.ForeignKey(SlackBotUserDMState)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=512)


class SlackBotGameState(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    game = models.ForeignKey(Game, db_index=True)
    state_class = models.CharField(max_length=64)
