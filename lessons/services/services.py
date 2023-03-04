import datetime
from authapp.models import User, Group
from lessons.models import Lesson
import pytz


def is_free_date_user(user, date, type):
    if type == 'group':
        lesson_dates = Lesson.objects.filter(group__students=user).all().values('date')
    else:
        lesson_dates = Lesson.objects.filter(teacher=user).all().values('date')
    for lesson_date in lesson_dates:
        dt = lesson_date.get('date')
        dt_plus_hour = dt + datetime.timedelta(hours=1)
        dt_minus_hour = dt - datetime.timedelta(hours=1)
        utc = pytz.UTC
        start_time = date.replace(tzinfo=utc)
        if dt <= start_time < dt_plus_hour:
            return False
        if dt_minus_hour < start_time <= dt:
            return False
    return True


def is_free_date(date, groups, teacher):
    student_list = [User.objects.get(pk=item) for item in groups]
    for student in student_list:
        student_free_date = is_free_date_user(user=student, date=date, type='group')
        if not student_free_date:
            return student_free_date

    teacher_free_date = is_free_date_user(user=teacher, date=date, type='teacher')
    return teacher_free_date
