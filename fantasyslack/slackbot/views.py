from pprint import pformat

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect

from fantasyslack import settings
from fantasyslack.slackbot.mongo import MongoDAO
from fantasyslack.slackbot.slack import SlackDAO
from fantasyslack.slackbot.factory import SlackMessageFactory, SlackUserFactory
from fantasyslack.slackbot.stats import StatReactions, StatChattyKathy, StatEmojiMaster, StatShouter, StatEditor


class HomeView(View):
    def get(self, request):
        return redirect('messages')


class MessagesList(View):
    url_name = 'messages-list'

    def get(self, request):
        mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
        slack_dao = SlackDAO(settings.SLACK_API_TOKEN)
        slack_message_factory = SlackMessageFactory(mongo_dao, slack_dao)
        messages = slack_message_factory.get(filter_dict={'$and': [{'type': {'$ne': 'reconnect_url'}}, {'type': {'$ne': 'presence_change'}}]})

        return render_to_response('slackbot/messages-list.jinja', {
            'messages': messages,
            'pformat': pformat,
            'getattr': getattr,
            'url_name': self.url_name
        })


class MessagesDetail(View):
    url_name = 'messages-detail'

    def get(self, request, object_id):
        mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
        slack_dao = SlackDAO(settings.SLACK_API_TOKEN)
        slack_message_factory = SlackMessageFactory(mongo_dao, slack_dao)
        message = slack_message_factory.get(object_id)

        if not message:
            raise Http404('message does not exist')

        return render_to_response('slackbot/messages-detail.jinja', {
            'object_id': object_id,
            'messages': [message],
            'pformat': pformat,
            'getattr': getattr,
            'url_name': self.url_name
        })


class StatsList(View):
    url_name = 'stats-list'

    def get(self, request):
        mongo_dao = MongoDAO(settings.MONGO_HOST, settings.MONGO_DATABASE)
        slack_dao = SlackDAO(settings.SLACK_API_TOKEN)
        slack_message_factory = SlackMessageFactory(mongo_dao, slack_dao)
        slack_user_factory = SlackUserFactory(mongo_dao, slack_dao)
        messages = slack_message_factory.get(filter_dict={'$and': [{'type': {'$ne': 'reconnect_url'}}, {'type': {'$ne': 'presence_change'}}]})
        users = slack_user_factory.create_all()

        stat_list = [StatReactions, StatChattyKathy, StatEmojiMaster, StatShouter, StatEditor]

        stats = {}

        for stat in stat_list:
            stats[stat.name] = stat(slack_message_factory).compute(messages, users)

        return render_to_response('slackbot/stats-list.jinja', {
            'stats': stats,
            'users': users,
            'url_name': self.url_name
        })


