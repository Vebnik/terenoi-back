import datetime
from authapp.models import User, Group
from lessons.models import Lesson
from lessons.services import current_date
from django.conf import settings
import pytz


def is_free_date(request_date, groups):
    date = datetime.datetime.strptime(request_date, settings.REST_FRAMEWORK.get('DATETIME_FORMAT'))
    student_list = [User.objects.get(pk=item) for item in groups]
    for student in student_list:
        groups = Group.objects.filter(students=student).all()
        for group in groups:
            lesson_dates = Lesson.objects.filter(group=group).all().values('date')
            for lesson_date in lesson_dates:
                student_lesson_date = current_date(student, lesson_date.get('date'))
                end_student_lesson_date = current_date(student, lesson_date.get('date') + datetime.timedelta(hours=1))
                utc = pytz.UTC
                start_time = date.replace(tzinfo=utc)
                if student_lesson_date <= start_time < end_student_lesson_date:
                    return False
    return True
