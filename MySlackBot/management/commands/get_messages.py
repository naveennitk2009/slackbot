__author__ = 'naveenkumar'

from django.core.management import BaseCommand
from MySlackBot.module import SlackBot
from django.conf import settings

class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        sbot = SlackBot(settings={'TOKEN': settings.TOKEN})
        sbot.get_messages_from_imcs()