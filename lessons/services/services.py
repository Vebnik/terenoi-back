from datetime import datetime
from authapp.models import User, Group
from lessons.models import Lesson
from lessons.services import current_date
from django.conf import settings


def is_free_date(request_date, groups):
    date = datetime.strptime(request_date, settings.REST_FRAMEWORK.get('DATETIME_FORMAT'))
    student_list = [User.objects.get(pk=item.get('pk')) for item in groups]
    for student in student_list:
        groups = Group.objects.filter(students=student).all()
        for group in groups:
            lesson_dates = Lesson.objects.filter(group=group).all().values('date')
            for lesson_date in lesson_dates:
                if current_date(student, lesson_date.get('date')) == current_date(student, date):
                    return False
    return True
