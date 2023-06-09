import re, datetime as dt
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, QuerySet
from dateutil import parser, tz
from datetime import time as parse_time

from authapp.models import User
from lessons.models import Schedule, Subject, WeekDays


class TeacherQueryParams:

    __slots__ = ('weekday', 'time', 'range', 'subject', 'teacher')

    def __init__(self, params) -> None:
        self.weekday = params.get('weekday', '')
        self.time = params.get('time', '')
        self.range = params.get('range', '')
        self.subject = params.get('subject', '')
        self.teacher = params.get('teacher', '')

    def __str__(self) -> str:
        return f'{self.weekday=} {self.range=} {self.time=} {self.subject=} {self.teacher=}'


class Utils:

    @staticmethod
    def phone_clener(phone):
        return re.sub(r'[^\d]', '', phone)

    @staticmethod
    def get_schdule_context():
        return {
            'teachers': User.objects.filter(is_teacher=True),
        }

    @staticmethod
    def serialize_date(config):
        time = config.get('lesson_start')
        date = config.get('date_start')

        start_date = [*map(int, date.split('-'))]
        time = [*map(int, time.split(':'))]

        return dt.datetime(start_date[0], start_date[1], start_date[2],
                           time[0], time[1])

    @staticmethod
    def serialize_only_date(date_str):
        start_date = [*map(int, date_str.split('-'))]
        return dt.date(start_date[0], start_date[1], start_date[2])

    @staticmethod
    def normalize_date(date):
        date = [*map(int, date.split('-'))]
        return dt.date(date[0], date[1], date[2])

    @staticmethod
    def normalize_time(time):
        time = [*map(int, time.split(':'))]
        return dt.time(time[0], time[1])


class QueryParams:

    __slots__ = ('sort','sortColumn','q','page','status','perPage','lessons','currentBalance', 'id', 'all')

    def __init__(self, params: str) -> None:
        self.id = params.get('id', None)
        self.sort = params.get('sort', 'desc')
        self.sortColumn = params.get('sortColumn', 'id')
        self.q = params.get('q', '')
        self.page = params.get('page', 1)
        self.status = params.get('status', '')
        self.perPage = params.get('perPage', 10)
        self.lessons = params.get('lessons', '')
        self.currentBalance = params.get('currentBalance', '')
        self.all = params.get('all', 0)

    def __str__(self) -> str:
        return f'{self.sort=} {self.sortColumn=} {self.q=} {self.page=} {self.status=} {self.perPage=} {self.lessons=} {self.currentBalance=}'


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Filter:
    @staticmethod
    def students_filter(queryset: QuerySet, params: QueryParams):

        if params.q:
            email = Q(email__icontains=params.q)
            phone = Q(phone__icontains=params.q)
            last_name = Q(last_name__icontains=params.q)
            first_name = Q(first_name__icontains=params.q)
            middle_name = Q(middle_name__icontains=params.q)
            username = Q(username__icontains=params.q)

            queryset = queryset.filter(
                email|phone|last_name|first_name|middle_name|username
            )

        if params.currentBalance:
            low_balance = params.currentBalance.split('-')[0]
            high_balance = params.currentBalance.split('-')[1]
            
            queryset = queryset.filter(
                balance_students__money_balance__lte=high_balance,
                balance_students__money_balance__gte=low_balance,
            )

        if params.status:
            queryset = queryset.filter(status=User.__getattribute__(User, params.status))

        if params.lessons:
            queryset = queryset.filter(
                balance_students__money_balance__lte=params.lessons,
            )

        if params.sortColumn:
            if params.sortColumn == 'id':
                queryset = queryset.order_by('-id')
            if params.sortColumn == 'fullname':
                order_name = f'{"-" if params.sort == "desc" else ""}first_name'
                queryset = queryset.order_by(order_name)
            if params.sortColumn == 'group':
                order_group = f'{"-" if params.sort == "desc" else ""}group_students'
                queryset = queryset.order_by(order_group)
            if params.sortColumn == 'subscription':
                order_subscription = f'{"-" if params.sort == "desc" else ""}subscription_students'
                queryset = queryset.order_by(order_subscription)
            if params.sortColumn == 'balance':
                queryset = sorted(
                    queryset, 
                    key=lambda el: el.balance_students.first().money_balance, 
                    reverse=(params.sort == "desc")
                )
            if params.sortColumn == 'status':
                order_status = f'{"-" if params.sort == "desc" else ""}status'
                queryset = queryset.order_by(order_status)
            
        return queryset

    @staticmethod
    def user_filter(params: QueryParams):
        
        if params.q == 'teacher':
            if params.id:
                query = User.objects.filter(is_teacher=True, id=params.id)
            else:
                query = User.objects.filter(is_teacher=True)
            return query
        if params.q == 'student':
            if params.id:
                query = User.objects.filter(is_student=True, id=params.id)
            else:
                query = User.objects.filter(is_student=True)
            return query
        if params.q == 'manager':
            if params.id:
                query = User.objects.filter(is_staff=True, id=params.id)
            else:
                query = User.objects.filter(is_staff=True)
            return query

        return User.objects.all()

    @staticmethod
    def free_teacher_filter(queryset: QuerySet, params: TeacherQueryParams):

        schedule = Schedule.objects.filter(is_completed=False)

        if params.range:
            try:
                range: list = params.range.split(',')
                schedule = schedule.filter(
                    Q(schedulesettings__near_lesson__date=range[0])|
                    Q(schedulesettings__last_lesson__date=range[1])
                )
            except IndexError: ...
        if params.weekday:
            weekadys = [WeekDays.objects.get(pk=num).pk for num in params.weekday.split(',')]
            schedule = schedule.filter(weekday__in=weekadys)
        if params.subject:
            subject = Subject.objects.get(pk=params.subject)
            schedule = schedule.filter(subject=subject)
        if params.time:
            time = parser.parse(params.time).time()
            time = parse_time(hour=(time.hour - 6), minute=time.minute).strftime('%H:%M')
            schedule = schedule.filter(
                schedulesettings__near_lesson__time__contains=time
            )

        # print(schedule)
        # print(set([item.pk for item in queryset]))
        # print(set([item.teacher.pk for item in schedule]))

        free_teachers_pk = set([item.pk for item in queryset]) - set([item.teacher.pk for item in schedule])

        # print([*free_teachers_pk])

        return queryset.filter(pk__in=[*free_teachers_pk])

    @staticmethod
    def group_filter(queryset: QuerySet, params: TeacherQueryParams):
        if params.teacher:
            queryset = queryset.filter(schedule_group__teacher=params.teacher)
        if params.weekday:
            weekadys = [WeekDays.objects.get(pk=num).pk for num in params.weekday.split(',')]
            queryset = queryset.filter(schedule_group__weekday__in=weekadys )
        if params.subject:
            subject = Subject.objects.get(pk=params.subject)
            queryset = queryset.filter(schedule_group__subject=subject )
        if params.time:
            time = parser.parse(params.time).time()
            time = parse_time(hour=(time.hour - 6), minute=time.minute).strftime('%H:%M')
            queryset = queryset.filter(
                schedule_group__schedulesettings__near_lesson__time__contains=time
            )


        return queryset