import logging
import os
import sys

from django.core.management import BaseCommand

from fantasyslack import settings
from fantasyslack.slackbot.rtmbot import RtmBot

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--daemon', action='store_true')

    def main_loop(self, bot):
        try:
            bot.start()
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            logging.exception('OOPS')

    def handle(self, *args, **options):
        bot = RtmBot(settings.SLACK_RTM_TOKEN, os.path.join(os.getcwd(), 'fantasyslack', 'slackbot', 'plugins'))

        if options['daemon']:
            import daemon

            with daemon.DaemonContext():
                self.main_loop(bot)

        self.main_loop(bot)
