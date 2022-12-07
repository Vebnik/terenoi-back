from django.core.management import BaseCommand

from authapp.services import get_cgi_alfa, auth_alfa_account


class Command(BaseCommand):

    def handle(self, *args, **options):
        token = auth_alfa_account()
        get_cgi_alfa(token)
