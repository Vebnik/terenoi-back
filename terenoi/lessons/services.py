import datetime
import pytz
from django.conf import settings
from voximplant.apiclient import VoximplantAPI, VoximplantException
import lessons
from authapp.decorators import create_voxi_file


def current_date(user, date):
    user_timezone = pytz.timezone(user.time_zone or settings.TIME_ZONE)
    return date.astimezone(user_timezone)


@create_voxi_file
def get_record(lesson_id, lesson_date):
    voxapi = VoximplantAPI("authapp/json/credentials.json")
    lesson = lessons.models.VoximplantRecordLesson.objects.filter(lesson__pk=lesson_id).first()
    if not lesson:
        return
    session_id = lesson.session_id
    lesson_from_date = lesson_date.day - 2
    lesson_to_date = lesson_date.day + 1
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
