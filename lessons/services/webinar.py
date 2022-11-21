from time import sleep

from authapp.models import Webinar, WebinarRecord
from lessons.services.pruffme import PruffMe


def create_new_webinar(webinar_pk):
    # lesson = Lesson.objects.get(pk=lesson_pk)
    webinar = None
    counter = 0
    while webinar is None and counter < 100:
        sleep(1)
        webinar = Webinar.objects.filter(pk=webinar_pk).first()
        counter += 1

    pruffme = PruffMe()

    webinar_response = pruffme.create_webinar(webinar)

    webinar.save_info(webinar_response)
    webinar.refresh_from_db()

    for student in webinar.lesson.students.all():
        student.create_participant(
            webinar,
            pruffme.create_participant(
                webinar,
                student
            ),
            'participant'
        )

    webinar.lesson.teacher.create_participant(
        webinar,
        pruffme.create_participant(
            webinar,
            webinar.lesson.teacher,
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
