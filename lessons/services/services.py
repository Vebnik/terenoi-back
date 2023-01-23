import datetime
from authapp.models import User, Group
from lessons.models import Lesson
from lessons.services import current_date
from django.conf import settings


def is_free_date(request_date, groups):
    date = datetime.datetime.strptime(request_date, settings.REST_FRAMEWORK.get('DATETIME_FORMAT'))
    student_list = [User.objects.get(pk=item) for item in groups]
    for student in student_list:
        groups = Group.objects.filter(students=student).all()
        for group in groups:
            lesson_dates = Lesson.objects.filter(group=group).all().values('date')
            for lesson_date in lesson_dates:
                student_lesson_date = current_date(student, lesson_date.get('date'))
                hour_1_lesson = student_lesson_date + datetime.timedelta(hours=1)
                fast_lesson_date = current_date(student, date)
                if student_lesson_date <= fast_lesson_date < hour_1_lesson:
                    return False
    return True
