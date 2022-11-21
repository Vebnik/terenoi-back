from authapp.models import Webinar, PruffmeAccount, WebinarRecord
from lessons.services.pruffme import PruffMe


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

    for student in lesson.students.all():
        student.create_participant(
            webinar,
            pruffme.create_participant(
                webinar,
                student
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


def get_webinar_records(webinar_list):
    pruffme = PruffMe()
    for webinar in webinar_list:
        webinar_record = pruffme.get_webinar_record(webinar)
        if len(webinar_record) > 0:
            WebinarRecord.objects.create(
                webinar=webinar,
                record=webinar_record
            )
