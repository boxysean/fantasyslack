from fantasyslack import settings
from fantasyslack.slackbot.models import SlackBotUserDMState, Player, SlackBotUserDMStateTable
from fantasyslack.slackbot.slack import SlackDAO


class FantasySlackBot(object):
    def __init__(self):
        self.slack_dao = SlackDAO(settings.SLACK_API_TOKEN)

    def direct_message(self, user, message):
        im_channel = self.slack_dao.get_im_channel_by_user_id(user.id)
        self.slack_dao.post_message(im_channel, message)

    def process_direct_message(self, user, message):
        states = SlackBotUserDMState.objects.filter(player__slack_user_id=user.id)
        latest_state = None

        if states:
            state = states.last()
            from pprint import pprint
            pprint(state.__dict__)
            if state.state_class == 'UserDMNewGameName':
                latest_state = UserDMNewGameName(self, state)
        else:
            latest_state = UserDMStartState(self, None)

        next_state = latest_state.process_direct_message(user, message)

        if next_state:
            player, _created = Player.objects.get_or_create(slack_user_id=user.id)
            SlackBotUserDMState(player=player, state_class=next_state.__unicode__()).save()


class FantasySlackBotState(object):
    def __init__(self, slackbot, state):
        self.slackbot = slackbot
        self.state = state

    def __unicode__(self):
        return self.__class__.__name__

    def process_direct_message(self, user, message):
        raise NotImplementedError()


class UserDMStartState(FantasySlackBotState):
    def process_direct_message(self, user, message):
        if message.lower().startswith('help'):
            self.slackbot.direct_message(user, 'You can ask me to start a new game by saying "Start"')
        elif 'start' in message.lower():
            self.slackbot.direct_message(user, 'Okay, what would you like to call your league? (If you\'d like me to pick one, just say "it\'s up to you, @fsb")')
            return UserDMNewGameName(self.slackbot, None)


class UserDMNewGameName(FantasySlackBotState):
    def process_direct_message(self, user, message):
        # entry = SlackBotUserDMStateTable.objects.filter(state=self.state, key='name').last()
        # new_game_name = entry.value
        new_game_name = message
        self.slackbot.direct_message(user, 'Okay, your league is called {new_game_name}'.format(**locals()))
        self.slackbot.direct_message(user, 'I\'m going to create a private channel for your league and invite you, one sec...')
        return GameConfigurationState(self.slackbot, None)


class GameConfigurationState(FantasySlackBotState):
    pass


class ConfigurationWizardState(FantasySlackBotState):
    def __init__(self, step):
        self.step = step

    def process_message(self, message):
        pass

    def next(self):
        if self.step == 4:
            return ConfigurationState()
        else:
            return ConfigurationWizardState(self.step + 1)

    def __unicode__(self):
        return '%s-%d' % (self.__class__.__name__, self.step)