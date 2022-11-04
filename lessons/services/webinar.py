from authapp.models import Webinar
from authapp.services.pruffme import PruffMe


def create_new_webinar(lesson):
    pruffme = PruffMe()

    webinar = Webinar.objects.create(
        name=f'webinar#{lesson.pk}',
        start_date=lesson.date,
        lesson=lesson
    )
    webinar_response = pruffme.create_webinar(webinar)

    webinar.save_info(webinar_response)
    webinar.refresh_from_db()

    lesson.student.create_participant(
        webinar,
        pruffme.create_participant(
            webinar,
            lesson.student
        ),
        'participant'
    )

    lesson.teacher.create_participant(
        webinar,
        pruffme.create_participant(
            webinar,
            lesson.teacher,
            'moderator'
        ),
        'moderator'
    )
