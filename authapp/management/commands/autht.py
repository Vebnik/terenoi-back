from django.core.management import BaseCommand

from authapp.models import User
from authapp.services import get_cgi_alfa, auth_alfa_account
from profileapp.models import ManagerToUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        # token = auth_alfa_account()
        # get_cgi_alfa(token)
        manager = User.objects.get(pk=4)
        for user in User.objects.filter(is_student=True):
            if not ManagerToUser.objects.filter(user=user).exists():
                ManagerToUser.objects.create(
                    manager=manager,
                    user=user
                )
