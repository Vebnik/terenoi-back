from django.core.management import BaseCommand

from authapp.models import User
from lessons.services.pruffme import PruffMe


class Command(BaseCommand):

    def handle(self, *args, **options):
        pruff_me = PruffMe()
        user = User.objects.filter(is_student=True, is_staff=False, is_superuser=False).first()
        # print(user)

        # webinar-create
        # webinar = Webinar.objects.create(
        #     name='testwebinar#3',
        #     start_date=datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)) + datetime.timedelta(hours=2)
        # )
        # webinar_response = pruff_me.create_webinar(webinar)
        # webinar.save_info(webinar_response)
        # webinar.refresh_from_db()
        # webinar = Webinar.objects.all().order_by('-id').first()
        # user.create_participant(
        #     webinar,
        #     pruff_me.create_student(
        #         webinar,
        #         user
        #     )
        # )

        print(pruff_me.get_webinar_record(object))
