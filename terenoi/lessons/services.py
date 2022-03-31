import datetime
import pytz
from django.conf import settings
from django.db.models import Sum
from voximplant.apiclient import VoximplantAPI, VoximplantException

import finance
import lessons
import notifications
from authapp.decorators import create_voxi_file
from authapp.services import send_transfer_lesson
from settings.models import RateTeachers


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
    lessons.models.Lesson.objects.create(teacher=lesson.teacher, student=lesson.student, topic=lesson.topic,
                                         subject=lesson.subject,
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


def payment_for_lesson(lesson):
    teacher_lesson = finance.models.HistoryPaymentTeacher.objects.filter(lesson=lesson)
    student_lesson = finance.models.HistoryPaymentStudent.objects.filter(lesson=lesson)
    student_payment = finance.models.HistoryPaymentStudent.objects.filter(student=lesson.student,
                                                                          subject=lesson.subject).aggregate(
        total_amount=Sum('amount'))
    student_count_lesson = finance.models.HistoryPaymentStudent.objects.filter(student=lesson.student,
                                                                               subject=lesson.subject).aggregate(
        total_count=Sum('lesson_count'))
    if not student_lesson:
        if student_count_lesson['total_count']:
            if student_count_lesson['total_count'] < 2:
                notifications.models.PaymentNotification.objects.create(to_user=lesson.student,
                                                                        type=notifications.models.PaymentNotification.AWAITING_PAYMENT)
            one_lesson_amount = student_payment['total_amount'] / student_count_lesson['total_count']
            finance.models.HistoryPaymentStudent.objects.create(student=lesson.student,
                                                                payment_date=datetime.datetime.now(),
                                                                amount=-one_lesson_amount, subject=lesson.subject,
                                                                lesson_count=-1, lesson=lesson, debit=True)
        else:
            finance.models.HistoryPaymentStudent.objects.create(student=lesson.student,
                                                                payment_date=datetime.datetime.now(),
                                                                amount=-0, subject=lesson.subject,
                                                                lesson_count=0, lesson=lesson, debit=True)
    if not teacher_lesson:
        default_rate = RateTeachers.objects.filter(subject=lesson.subject).first().rate
        rate = finance.models.TeacherRate.objects.filter(teacher=lesson.teacher, subject=lesson.subject).first()
        if not rate:
            finance.models.HistoryPaymentTeacher.objects.create(teacher=lesson.teacher,
                                                                payment_date=datetime.datetime.now(),
                                                                lesson=lesson, amount=default_rate, is_enrollment=True)
        else:
            finance.models.HistoryPaymentTeacher.objects.create(teacher=lesson.teacher,
                                                                payment_date=datetime.datetime.now(),
                                                                lesson=lesson, amount=rate.rate, is_enrollment=True)


def withdrawing_cancel_lesson(lesson, user):
    if user.is_student:
        current_date_lesson = current_date(user=user, date=lesson.date)
        current_date_user = current_date(user=user, date=datetime.datetime.now())
        hours = current_date_lesson-current_date_user
        timedel = datetime.timedelta(hours=4)
        if hours < timedel:
            student_lesson = finance.models.HistoryPaymentStudent.objects.filter(lesson=lesson)
            student_payment = finance.models.HistoryPaymentStudent.objects.filter(student=lesson.student,
                                                                                  subject=lesson.subject).aggregate(
                total_amount=Sum('amount'))
            student_count_lesson = finance.models.HistoryPaymentStudent.objects.filter(student=lesson.student,
                                                                                       subject=lesson.subject).aggregate(
                total_count=Sum('lesson_count'))
            if not student_lesson:
                if student_count_lesson['total_count']:
                    if student_count_lesson['total_count'] < 2:
                        notifications.models.PaymentNotification.objects.create(to_user=lesson.student,
                                                                                type=notifications.models.PaymentNotification.AWAITING_PAYMENT)
                    one_lesson_amount = student_payment['total_amount'] / student_count_lesson['total_count']
                    finance.models.HistoryPaymentStudent.objects.create(student=lesson.student,
                                                                        payment_date=datetime.datetime.now(),
                                                                        amount=-one_lesson_amount,
                                                                        subject=lesson.subject,
                                                                        lesson_count=-1, lesson=lesson, debit=True)