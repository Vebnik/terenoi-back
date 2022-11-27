from django.db.models import Q
import lessons
from notifications.models import Notification


def create_lesson_notifications(lesson_status, students, date, teacher, teacher_status, lesson_id):
    for student in students.all():
        if lesson_status == lessons.models.Lesson.SCHEDULED:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_SCHEDULED))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_SCHEDULED,
                                            lesson_id=lesson_id)
            if Notification.objects.filter(
                    (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_SCHEDULED))).first():
                pass
            else:
                Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_SCHEDULED,
                                            lesson_id=lesson_id)

        if teacher_status:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_PROGRESS))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_PROGRESS,
                                            lesson_id=lesson_id)

        if lesson_status == lessons.models.Lesson.CANCEL:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_CANCEL))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_CANCEL,
                                            lesson_id=lesson_id)

        if lesson_status == lessons.models.Lesson.REQUEST_RESCHEDULED:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(
                        type=Notification.LESSON_REQUEST_RESCHEDULED))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date,
                                            type=Notification.LESSON_REQUEST_RESCHEDULED, lesson_id=lesson_id)

        if lesson_status == lessons.models.Lesson.RESCHEDULED:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_RESCHEDULED))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_RESCHEDULED,
                                            lesson_id=lesson_id)

        if lesson_status == lessons.models.Lesson.REQUEST_CANCEL:
            if Notification.objects.filter(
                    (Q(to_user=student) & Q(lesson_date=date) & Q(type=Notification.LESSON_REQUEST_CANCEL))).first():
                pass
            else:
                Notification.objects.create(to_user=student, lesson_date=date, type=Notification.LESSON_REQUEST_CANCEL,
                                            lesson_id=lesson_id)

    if lesson_status == lessons.models.Lesson.SCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_SCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_SCHEDULED,lesson_id=lesson_id)

    if teacher_status:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_PROGRESS))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_PROGRESS,lesson_id=lesson_id)

    if lesson_status == lessons.models.Lesson.CANCEL:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_CANCEL))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_CANCEL,lesson_id=lesson_id)

    if lesson_status == lessons.models.Lesson.REQUEST_RESCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_REQUEST_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_REQUEST_RESCHEDULED,lesson_id=lesson_id)


    if lesson_status == lessons.models.Lesson.RESCHEDULED:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_RESCHEDULED))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_RESCHEDULED,lesson_id=lesson_id)

    if lesson_status == lessons.models.Lesson.REQUEST_CANCEL:
        if Notification.objects.filter(
                (Q(to_user=teacher) & Q(lesson_date=date) & Q(type=Notification.LESSON_REQUEST_CANCEL))).first():
            pass
        else:
            Notification.objects.create(to_user=teacher, lesson_date=date, type=Notification.LESSON_REQUEST_CANCEL,
                                        lesson_id=lesson_id)

