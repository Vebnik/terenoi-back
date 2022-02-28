import datetime
import pytz
from django.conf import settings
from voximplant.apiclient import VoximplantAPI, VoximplantException
import lessons
from authapp.decorators import create_voxi_file
from authapp.services import send_transfer_lesson



def current_date(user, date):
    user_timezone = pytz.timezone(user.time_zone or settings.TIME_ZONE)
    return date.astimezone(user_timezone)


@create_voxi_file
def get_record(lesson_id, lesson_date):
    voxapi = VoximplantAPI("authapp/json/credentials.json")
    lesson_list = lessons.models.VoximplantRecordLesson.objects.filter(lesson__pk=lesson_id)
    if not lesson_list:
        return
    for lesson in lesson_list:
        session_id = lesson.session_id
        lesson_from_date = lesson_date.day
        lesson_to_date = lesson_date.day
        FROM_DATE = datetime.datetime(lesson_date.year, lesson_date.month, lesson_from_date, 0, 0, 0, tzinfo=pytz.utc)
        TO_DATE = datetime.datetime(lesson_date.year, lesson_date.month, lesson_to_date, 23, 59, 59, tzinfo=pytz.utc)
        WITH_CALLS = True
        WITH_RECORDS = True
        record = ''
        try:
            res = voxapi.get_call_history(FROM_DATE,
                                          TO_DATE,
                                          with_calls=WITH_CALLS,
                                          with_records=WITH_RECORDS,
                                          call_session_history_id=session_id
                                          )
            record = res.get('result')[0].get('records')[0].get('record_url')
            lesson.record = record
            lesson.save()
        except VoximplantException as e:
            print("Error: {}".format(e.message))


def request_transfer(user, lesson, manager, transfer_comment, send_func, date):
    if user.is_student or user.is_teacher:
        if lesson.lesson_status == lessons.models.Lesson.SCHEDULED:
            send_func(manager, lesson)
    lessons.models.ManagerRequests.objects.create(lesson=lesson, manager=manager, user=user,
                                                  type=lessons.models.ManagerRequests.REQUEST_RESCHEDULED,
                                                  comment=transfer_comment, date=date)


def request_cancel(user, lesson, manager, transfer_comment, send_func):
    if user.is_student or user.is_teacher:
        if lesson.lesson_status == lessons.models.Lesson.SCHEDULED:
            send_func(manager, lesson)
    lessons.models.ManagerRequests.objects.create(lesson=lesson, manager=manager, user=user,
                                                  type=lessons.models.ManagerRequests.REQUEST_CANCEL,
                                                  comment=transfer_comment)


def send_transfer(manager, lesson, send_func):
    send_func(manager, lesson)
    manager_req = lessons.models.ManagerRequests.objects.filter(lesson=lesson).first()
    lessons.models.Lesson.objects.create(teacher=lesson.teacher, student=lesson.student, topic=lesson.topic, subject=lesson.subject,
                          date=manager_req.date)
    if manager_req:
        manager_req.is_resolved = True
        manager_req.type = lessons.models.ManagerRequests.RESCHEDULED
        manager_req.save()


def send_cancel(manager, lesson, send_func):
    send_func(manager, lesson)
    manager_req = lessons.models.ManagerRequests.objects.filter(lesson=lesson).first()
    if manager_req:
        manager_req.is_resolved = True
        manager_req.type = lessons.models.ManagerRequests.CANCEL
        manager_req.save()
