from django.core.management.base import BaseCommand

from dns.networking import run


class Command(BaseCommand):

    help = 'Runs TCP/UDP DNS protocol handler.'

    def handle(self, *args, **options):
        run()
