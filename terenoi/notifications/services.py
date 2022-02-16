from django.db.models import Q
import lessons
from notifications.models import Notification


def create_lesson_notifications(lesson_status, student, date, teacher, teacher_status):
    if lesson_status == lessons.models.Lesson.SCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_SCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_SCHEDULED)
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_SCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_SCHEDULED)

    if teacher_status:
        if Notification.objects.filter(
                (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_PROGRESS))).first():
            pass
        else:
            Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_PROGRESS)
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_PROGRESS))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_PROGRESS)

    if lesson_status == lessons.models.Lesson.CANCEL:
        if Notification.objects.filter(
                (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_CANCEL))).first():
            pass
        else:
            Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_CANCEL)
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_CANCEL))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_CANCEL)
    if lesson_status == lessons.models.Lesson.REQUEST_RESCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_REQUEST_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_REQUEST_RESCHEDULED)
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_REQUEST_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_REQUEST_RESCHEDULED)

    if lesson_status == lessons.models.Lesson.RESCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_RESCHEDULED)
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_RESCHEDULED)
