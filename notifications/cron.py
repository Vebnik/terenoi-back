import datetime
from django.db.models import Q
from lessons.models import Lesson
from lessons.services import current_date
from notifications.models import Notification


def add_note_cron():
    lessons = Lesson.objects.filter(lesson_status=Lesson.SCHEDULED).select_related()
    transfer_lessons = Lesson.objects.filter(lesson_status=Lesson.RESCHEDULED).select_related()
    for i in lessons:
        day_student = current_date(i.student, i.date)
        day_teacher = current_date(i.teacher, i.date)
        day_student_now = current_date(i.student, datetime.datetime.now())
        day_teacher_now = current_date(i.teacher, datetime.datetime.now())
        student_timedelta = day_student - day_student_now
        teacher_timedelta = day_teacher - day_teacher_now
        student_timedelta_str = str(student_timedelta)[2:4]
        if student_timedelta_str == '15':
            if Notification.objects.filter(
                    (Q(to_user=i.student) & Q(lesson_date=i.date) & Q(type=Notification.LESSON_COMING_SOON))).first():
                pass
            else:
                Notification.objects.create(to_user=i.student, lesson_date=i.date, type=Notification.LESSON_COMING_SOON)
        teacher_timedelta_str = str(teacher_timedelta)[2:4]
        if teacher_timedelta_str == '15':
            if Notification.objects.filter(
                    (Q(to_user=i.teacher) & Q(lesson_date=i.date) & Q(type=Notification.LESSON_COMING_SOON))).first():
                pass
            else:
                Notification.objects.create(to_user=i.teacher, lesson_date=i.date, type=Notification.LESSON_COMING_SOON)
    for i in transfer_lessons:
        day_student = current_date(i.student, i.transfer_date)
        day_teacher = current_date(i.teacher, i.transfer_date)
        day_student_now = current_date(i.student, datetime.datetime.now())
        day_teacher_now = current_date(i.teacher, datetime.datetime.now())
        student_timedelta = day_student - day_student_now
        teacher_timedelta = day_teacher - day_teacher_now
        student_timedelta_str = str(student_timedelta)[2:4]
        if student_timedelta_str == '15':
            if Notification.objects.filter(
                    (Q(to_user=i.student) & Q(lesson_date=i.transfer_date) & Q(
                        type=Notification.LESSON_COMING_SOON))).first():
                pass
            else:
                Notification.objects.create(to_user=i.student, lesson_date=i.transfer_date,
                                            type=Notification.LESSON_COMING_SOON)
        teacher_timedelta_str = str(teacher_timedelta)[2:4]
        if teacher_timedelta_str == '15':
            if Notification.objects.filter(
                    (Q(to_user=i.teacher) & Q(lesson_date=i.transfer_date) & Q(
                        type=Notification.LESSON_COMING_SOON))).first():
                pass
            else:
                Notification.objects.create(to_user=i.teacher, lesson_date=i.transfer_date,
                                            type=Notification.LESSON_COMING_SOON)


