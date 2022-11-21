import datetime
import http

import pytz
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.generic import TemplateView

from authapp.models import User, Webinar, PruffmeAccount
from authapp.services import send_transfer_lesson, send_accept_transfer_lesson, send_reject_transfer_lesson, \
    send_cancel_lesson
from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework, \
    ManagerRequestsRejectTeacher, TeacherWorkHours, TeacherWorkHoursSettings, Feedback
from lessons.serializers import UserLessonsSerializer, VoxiTeacherInfoSerializer, VoxiStudentInfoSerializer, \
    UserLessonsCreateSerializer, TeacherStatusUpdate, StudentStatusUpdate, LessonMaterialsDetail, LessonHomeworksDetail, \
    LessonEvaluationSerializer, LessonStudentEvaluationAddSerializer, \
    LessonTeacherEvaluationAddSerializer, LessonTransferSerializer, LessonEvaluationQuestionsSerializer, \
    LessonRateHomeworkDetail, UserClassesSerializer, HomepageStudentSerializer, HomepageTeacherSerializer, \
    StudentsSerializer, StudentDetailSerializer, HomeworksSerializer, TopicSerializer, TeacherScheduleCreateSerializer, \
    TeacherScheduleDetailSerializer, StudentsActiveSerializer, TeacherScheduleNoneDetailSerializer, \
    TeacherRecruitingSerializer
from lessons.services import request_transfer, send_transfer, request_cancel, send_cancel, current_date, \
    withdrawing_cancel_lesson
from notifications.models import ManagerNotification, HomeworkNotification, LessonRateNotification, Notification
from profileapp.models import Subject, ManagerToUser, GlobalUserPurpose, GlobalPurpose
from profileapp.serializers import PurposeSerializer, GlobalPurposeSerializer
from settings.models import WeekDays


class AllUserLessonsListView(generics.ListAPIView):
    """Список всех уроков пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            queryset = Lesson.objects.filter(students=self.request.user).order_by('date').select_related()
        else:
            queryset = Lesson.objects.filter(teacher=self.request.user).order_by('date').select_related()
        return queryset


class AllUserClassesListView(generics.ListAPIView):
    """Список всех прошедших уроков пользователя и одного будущего"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserClassesSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            time_delta = datetime.timedelta(days=1)
            day_now = datetime.datetime.now()
            lesson_query = Lesson.objects.filter(students=self.request.user,
                                                 date__lte=day_now.date() + time_delta).order_by('-date')
            lesson_shedule = Lesson.objects.filter(
                Q(students=self.request.user) & Q(lesson_status=Lesson.SCHEDULED)).order_by('date')[:1].select_related()
            if lesson_shedule in lesson_query:
                lesson_list = lesson_query.dates('date', 'day').order_by('-date')
            else:
                lesson_list = lesson_shedule.values('date').union(lesson_query.values('date')).order_by('-date')
            date_list = []
            for item in lesson_list:
                date = current_date(user=self.request.user, date=item.get('date')).date()
                if date in date_list:
                    pass
                else:
                    date_list.append(current_date(user=self.request.user, date=item.get('date')).date())

            queryset = date_list
            return queryset


class StudentsListView(APIView):
    """Данные учиников учителя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        serializer = StudentsSerializer(user)
        return Response(serializer.data)


class StudentsActiveListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        serializer = StudentsActiveSerializer(user)
        return Response(serializer.data)


class TopicUpdateView(generics.UpdateAPIView):
    """Обновление тем уроков"""
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer
    queryset = Lesson.objects.all()

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            for item in self.request.data:
                lesson = Lesson.objects.filter(pk=item.get('lesson_id', None)).first()
                lesson.topic = item.get('topic', None)
                lesson.save()
            return Response({'message': 'Темы уроков добавлены'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Что-то пошло не так, попробуйте еще раз'}, status=status.HTTP_400_BAD_REQUEST)


class PurposeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GlobalPurposeSerializer

    def get_queryset(self):
        if self.request.query_params:
            queryset = GlobalPurpose.objects.filter(subject__name=self.request.query_params.get('subject'))
            return queryset


class PurposeUpdateView(generics.UpdateAPIView):
    """Обновдение цели ученика"""
    permission_classes = [IsAuthenticated]
    serializer_class = PurposeSerializer
    queryset = GlobalUserPurpose.objects.all()

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            purpose = GlobalUserPurpose.objects.filter(user__pk=int(self.kwargs.get('pk')),
                                                       subject__name=self.request.query_params.get('subject')).first()
            purpose_add = GlobalPurpose.objects.filter(pk=int(self.request.data.get('pk'))).first()
            if not purpose:
                student = User.objects.filter(pk=int(self.kwargs.get('pk'))).first()
                GlobalUserPurpose.objects.create(user=student,
                                                 subject=purpose_add.subject,
                                                 purpose=purpose_add)
            else:
                purpose.purpose = purpose_add
                purpose.save()
            return Response({'message': 'Цель ученика добавлена'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Что-то пошло не так, попробуйте еще раз'}, status=status.HTTP_400_BAD_REQUEST)


class HomeworksView(APIView):
    """ Домашние работы учеников"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        if not self.request.query_params:
            serializer = HomeworksSerializer(user)
            return Response(serializer.data)
        else:
            serializer = HomeworksSerializer(user, context={'params': self.request.query_params})
            return Response(serializer.data)


class StudentsDetailView(APIView):
    """Данные одного ученика"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request, pk):
        user = self.get_object()
        if not self.request.query_params:
            serializer = StudentDetailSerializer(user, context={'pk': pk})
            return Response(serializer.data)
        else:
            serializer = StudentDetailSerializer(user,
                                                 context={'pk': pk, 'params': self.request.query_params})
            return Response(serializer.data)


class StudentsRejectView(APIView):
    """Отказ от ученика"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            student = User.objects.filter(pk=pk).first()
            manager = ManagerToUser.objects.get(user=student).manager
            subject = self.request.data.get('subject')
            comment = self.request.data.get('comment')
            subject_name = Subject.objects.filter(name=subject).first()
            ManagerRequestsRejectTeacher.objects.create(manager=manager, student=student, old_teacher=self.request.user,
                                                        subject=subject_name, comment=comment)
            ManagerNotification.objects.create(manager=manager, type=ManagerNotification.REQUEST_REJECT_STUDENT)
            return Response({'message': 'Запрос на отказ ученика отправлен'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Что-то пошло не так, попробуйте еще раз'}, status=status.HTTP_400_BAD_REQUEST)


class UserLessonRetrieveView(generics.RetrieveAPIView):
    """Просмотр одного урока пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()


class UserLessonCreateView(generics.CreateAPIView):
    """Создание урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsCreateSerializer
    queryset = Lesson.objects.all()

    def post(self, request, *args, **kwargs):
        if self.request.data.get('subject'):
            subject = Subject.objects.filter(name=self.request.data.get('subject')).first()
            if subject is None:
                return Response({"message": "Такого предмета не существует."}, status=status.HTTP_404_NOT_FOUND)

        return super(UserLessonCreateView, self).post(request, *args, **kwargs)


class LessonTransferUpdateView(generics.UpdateAPIView):
    """Запрос на перенос урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = LessonTransferSerializer
    queryset = Lesson.objects.all()

    def update(self, request, *args, **kwargs):
        lesson_id = self.kwargs.get('pk')
        lesson = Lesson.objects.get(pk=lesson_id)
        manager = ManagerToUser.objects.get(user=self.request.user).manager
        if self.request.data.get('lesson_status') == Lesson.REQUEST_RESCHEDULED:
            request_transfer(self.request.user, lesson, manager, self.request.data.get('transfer_comment'),
                             send_transfer_lesson, self.request.data.get('transfer_date'))
            ManagerNotification.objects.create(manager=manager, type=ManagerNotification.REQUEST_LESSON_RESCHEDULED)
        elif self.request.data.get('lesson_status') == Lesson.RESCHEDULED:
            transfer = self.request.data.get('transfer')
            if transfer:
                send_transfer(manager, lesson, send_accept_transfer_lesson)
                return super(LessonTransferUpdateView, self).update(request, *args, **kwargs)
            else:
                send_reject_transfer_lesson(manager, lesson)
                return Response({'message': 'Запрос на перенос урока отклонен'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif self.request.data.get('lesson_status') == Lesson.REQUEST_CANCEL:
            withdrawing_cancel_lesson(lesson, self.request.user)
            request_cancel(self.request.user, lesson, manager, self.request.data.get('transfer_comment'),
                           send_cancel_lesson)
            ManagerNotification.objects.create(manager=manager, type=ManagerNotification.REQUEST_LESSON_CANCEL)
        elif self.request.data.get('lesson_status') == Lesson.CANCEL:
            transfer = self.request.data.get('transfer')
            if transfer:
                send_cancel(manager, lesson, send_accept_transfer_lesson)
                return super(LessonTransferUpdateView, self).update(request, *args, **kwargs)
            else:
                send_reject_transfer_lesson(manager, lesson)
                return Response({'message': 'Запрос на отмену урока отклонен'},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super(LessonTransferUpdateView, self).update(request, *args, **kwargs)


class LessonMaterialsAdd(generics.UpdateAPIView):
    """
    Добавление материалов урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()

    def update(self, request, *args, **kwargs):
        if self.request.FILES.getlist('material'):
            for material in self.request.FILES.getlist('material'):
                LessonMaterials.objects.create(lesson=self.get_object(), material=material)
        if self.request.data.get('text_material'):
            text = self.request.data.get('text_material')
            LessonMaterials.objects.create(lesson=self.get_object(), text_material=text)
        return super(LessonMaterialsAdd, self).update(request, *args, **kwargs)


class LessonHomeworksAdd(generics.UpdateAPIView):
    """
    Добавление домашних заданий урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()

    def update(self, request, *args, **kwargs):
        self.kwargs.get('pk')
        lesson = self.get_object()
        if self.request.FILES.getlist('homework'):
            for material in self.request.FILES.getlist('homework'):
                LessonHomework.objects.create(lesson=self.get_object(), homework=material)
        if self.request.data.get('text_homework'):
            text = self.request.data.get('text_homework')
            LessonHomework.objects.create(lesson=self.get_object(), text_homework=text)
        HomeworkNotification.objects.create(to_user=lesson.teacher, lesson_id=self.kwargs.get('pk'),
                                            type=HomeworkNotification.HOMEWORK_ADD)
        return super(LessonHomeworksAdd, self).update(request, *args, **kwargs)


class HomepageListView(APIView):
    """Домашняя страница пользователя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        if user.is_student:
            serializer = HomepageStudentSerializer(user)
            return Response(serializer.data)
        elif user.is_teacher:
            serializer = HomepageTeacherSerializer(user)
            return Response(serializer.data)


class LessonRateHomeworksAdd(generics.UpdateAPIView):
    """Оценка урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        rate = None
        rate_comment = None
        if self.request.data.get('rate'):
            rate = self.request.data.get('rate')
        if self.request.data.get('rate_comment'):
            rate_comment = self.request.data.get('rate_comment')
        LessonRateHomework.objects.create(lesson=self.get_object(), rate=rate, rate_comment=rate_comment)
        HomeworkNotification.objects.create(to_user=lesson.student, lesson_id=self.kwargs.get('pk'),
                                            type=HomeworkNotification.HOMEWORK_CHECK)
        return super(LessonRateHomeworksAdd, self).update(request, *args, **kwargs)


class TeacherScheduleCreateView(generics.CreateAPIView):
    """Создание урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherScheduleCreateSerializer
    queryset = TeacherWorkHours.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            if self.request.data:
                teacher_hours = TeacherWorkHours.objects.filter(teacher=self.request.user).first()
                if teacher_hours:
                    pass
                else:
                    teacher_hours = TeacherWorkHours.objects.create(teacher=self.request.user)
                for req in self.request.data:
                    if req.get('daysOfWeek'):
                        for days in req.get('daysOfWeek'):
                            for period in req.get('periods'):
                                if period.get('startTime') == '' or period.get('endTime') == '':
                                    weekday = WeekDays.objects.filter(american_number=int(days)).first()
                                    TeacherWorkHoursSettings.objects.create(teacher_work_hours=teacher_hours,
                                                                            weekday=weekday)
                                else:
                                    weekday = WeekDays.objects.filter(american_number=int(days)).first()
                                    TeacherWorkHoursSettings.objects.create(teacher_work_hours=teacher_hours,
                                                                            weekday=weekday,
                                                                            start_time=period.get('startTime'),
                                                                            end_time=period.get('endTime'))

                return Response({'message': 'Рабочие часы добавлены'},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Что-то пошло не так, попробуйте еще раз'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TeacherScheduleListView(generics.ListAPIView):
    """Список рабочих часов учителя"""
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherScheduleCreateSerializer

    def get_queryset(self):
        th_work = TeacherWorkHours.objects.filter(teacher=self.request.user).first()
        queryset = TeacherWorkHoursSettings.objects.filter(teacher_work_hours=th_work)
        return queryset


class TeacherScheduleDetailListView(generics.ListAPIView):
    """Список рабочих часов учителя"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        th_work = TeacherWorkHours.objects.filter(teacher=self.request.user).first()
        queryset = TeacherWorkHoursSettings.objects.filter(teacher_work_hours=th_work).distinct('weekday')
        return queryset

    def get(self, request, *args, **kwargs):
        if not self.get_queryset():
            weekdays = WeekDays.objects.all()
            serializer = TeacherScheduleNoneDetailSerializer(weekdays, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            serializer = TeacherScheduleDetailSerializer(self.get_queryset(), many=True,
                                                         context={'teacher': self.request.user})
            return JsonResponse(serializer.data, safe=False)


class TeacherScheduleUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherScheduleCreateSerializer

    def get_object(self):
        schedule = TeacherWorkHours.objects.filter(teacher=self.request.user).first()
        return schedule

    def update(self, request, *args, **kwargs):
        try:
            TeacherWorkHoursSettings.objects.filter(teacher_work_hours=self.get_object()).delete()
            for req in self.request.data:
                if req.get('daysOfWeek'):
                    for days in req.get('daysOfWeek'):
                        for period in req.get('periods'):
                            if period.get('startTime') == '' or period.get('endTime') == '':
                                weekday = WeekDays.objects.filter(american_number=int(days)).first()
                                TeacherWorkHoursSettings.objects.create(teacher_work_hours=self.get_object(),
                                                                        weekday=weekday)
                            else:
                                weekday = WeekDays.objects.filter(american_number=int(days)).first()
                                TeacherWorkHoursSettings.objects.create(teacher_work_hours=self.get_object(),
                                                                        weekday=weekday,
                                                                        start_time=period.get('startTime'),
                                                                        end_time=period.get('endTime'))

            return Response({'message': 'Данные изменены'},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Что-то пошло не так, попробуйте еще раз'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TeacherRecruitingListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherRecruitingSerializer

    def get_object(self):
        user = User.objects.get(username=self.request.user)
        return user


class TeacherRecruitingUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherRecruitingSerializer

    def get_object(self):
        user = User.objects.get(username=self.request.user)
        return user


class LessonMaterialsRetrieveView(generics.RetrieveAPIView):
    """
    Получение материалов урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonMaterialsDetail
    queryset = Lesson.objects.all()


class LessonHomeworksRetrieveView(generics.RetrieveAPIView):
    """
    Получение домашних заданий урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonHomeworksDetail
    queryset = Lesson.objects.all()


class LessonRateHomeworkRetrieveView(generics.RetrieveAPIView):
    """
    Получение оценки урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonRateHomeworkDetail
    queryset = Lesson.objects.all()


class LessonEvaluationRetrieveView(generics.ListAPIView):
    """
    Просмотр оценки урока
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonEvaluationSerializer

    def get_queryset(self):
        return Feedback.objects.filter(lesson_id=self.kwargs.get('pk'))


class LessonEvaluationUpdateView(generics.CreateAPIView):
    """
    Добавление оценки урока
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        lesson = Lesson.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.is_student:
            if int(self.request.data.get('student_evaluation')) > 8:
                manager = ManagerToUser.objects.filter(user=lesson.teacher).first()
                LessonRateNotification.objects.create(to_user=lesson.teacher, lesson_id=self.kwargs.get('pk'),
                                                      type=LessonRateNotification.LESSON_RATE_HIGH)
                if manager:
                    ManagerNotification.objects.create(manager=manager.manager, to_user=lesson.teacher,
                                                       lesson_id=self.kwargs.get('pk'),
                                                       type=ManagerNotification.LESSON_RATE_HIGH)
            elif int(self.request.data.get('student_evaluation')) <= 3:
                manager = ManagerToUser.objects.filter(user=lesson.teacher).first()
                LessonRateNotification.objects.create(to_user=lesson.teacher, lesson_id=self.kwargs.get('pk'),
                                                      type=LessonRateNotification.LESSON_RATE_LOW)
                if manager:
                    ManagerNotification.objects.create(manager=manager.manager, to_user=lesson.teacher,
                                                       lesson_id=self.kwargs.get('pk'),
                                                       type=ManagerNotification.LESSON_RATE_LOW)

            return LessonStudentEvaluationAddSerializer
        else:
            if int(self.request.data.get('teacher_evaluation')) > 8:
                manager = ManagerToUser.objects.filter(user=lesson.student).first()
                LessonRateNotification.objects.create(to_user=lesson.student, lesson_id=self.kwargs.get('pk'),
                                                      type=LessonRateNotification.LESSON_RATE_HIGH)
                if manager:
                    ManagerNotification.objects.create(manager=manager.manager, to_user=lesson.student,
                                                       lesson_id=self.kwargs.get('pk'),
                                                       type=ManagerNotification.LESSON_RATE_HIGH)
            elif int(self.request.data.get('teacher_evaluation')) <= 3:
                manager = ManagerToUser.objects.filter(user=lesson.student).first()
                LessonRateNotification.objects.create(to_user=lesson.student, lesson_id=self.kwargs.get('pk'),
                                                      type=LessonRateNotification.LESSON_RATE_LOW)
                if manager:
                    ManagerNotification.objects.create(manager=manager.manager, to_user=lesson.student,
                                                       lesson_id=self.kwargs.get('pk'),
                                                       type=ManagerNotification.LESSON_RATE_LOW)
            return LessonTeacherEvaluationAddSerializer

    def perform_create(self, serializer):
        feedback_item = serializer.save()
        feedback_item.lesson_id = self.kwargs.get('pk')
        feedback_item.save()


class LessonEvaluationQuestionsRetrieveView(generics.RetrieveAPIView):
    """Получение вопросов для оценки урока учителем"""
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = LessonEvaluationQuestionsSerializer


class VoxiTeacherInfoRetrieveView(generics.RetrieveAPIView):
    """Информация об аккаунте учителя в voxiplant и статусе его готовности"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = VoxiTeacherInfoSerializer


class VoxiStudentInfoRetrieveView(generics.RetrieveAPIView):
    """Информация об аккаунте студента в voxiplant и статусе его готовности"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = VoxiStudentInfoSerializer


class LessonUserStatusUpdateView(generics.UpdateAPIView):
    """Обновление статуса пользователя в уроке"""
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_teacher:
            return TeacherStatusUpdate
        elif self.request.user.is_student:
            return StudentStatusUpdate

    def update(self, request, *args, **kwargs):
        if self.request.user.is_teacher:
            lesson = Lesson.objects.filter(pk=int(self.kwargs.get('pk'))).first()
            lesson.teacher_entry_date = current_date(user=self.request.user, date=datetime.datetime.now())
            lesson.save()
        else:
            lesson = Lesson.objects.filter(pk=int(self.kwargs.get('pk'))).first()
            lesson.student_entry_date = current_date(user=self.request.user, date=datetime.datetime.now())
            lesson.save()
        return super(LessonUserStatusUpdateView, self).update(request, *args, **kwargs)


class LessonUpdateView(generics.UpdateAPIView):
    """Обновление данных урока"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserLessonsSerializer
    queryset = Lesson.objects.all()


class CreateVoxiCallData(APIView):
    """Получение данных из Вокса"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        lesson_id = self.request.query_params.get('lesson_id')
        session_id = self.request.query_params.get('session_id')
        try:
            lesson = Lesson.objects.filter(pk=int(lesson_id)).first()
            VoximplantRecordLesson.objects.create(lesson=lesson, session_id=int(session_id))
            return Response({'message': 'Данные добавлены'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Данные не добавлены'}, status=status.HTTP_404_NOT_FOUND)


class LessonTemplateView(TemplateView):
    template_name = 'lessons/lesson.html'

    def get_context_data(self, **kwargs):
        # get current user
        context_data = super().get_context_data(**kwargs)
        current_webinar = Webinar.objects.all().order_by('-id').first()
        current_pruffme_account = PruffmeAccount.objects.filter(webinar=current_webinar).order_by('-id').first()
        context_data['webinar_hash'] = current_webinar.hash
        context_data['participant_name'] = current_pruffme_account.name
        context_data['participant_session'] = current_pruffme_account.session
        print(current_webinar.__dict__)
        return context_data


class LessonLinkGetter(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        lesson_id = self.kwargs.get('lesson_id')
        current_webinar = Webinar.objects.filter(lesson_id=lesson_id).first()
        if current_webinar:
            current_pruffme_account = PruffmeAccount.objects.filter(
                webinar=current_webinar,
                user_id=self.request.user.pk
            ).first()
            if current_pruffme_account:
                return Response(
                    data={
                        'url': f'https://pruffme.com/webinar/?id={current_webinar.hash}#session={current_pruffme_account.session}',
                        'stop_id': 'just-to-study-lesson-done'
                    },
                    status=http.HTTPStatus.OK
                )
        return Response(
            data={},
            status=http.HTTPStatus.FORBIDDEN
        )


class LessonDoneTemplateView(TemplateView):
    template_name = 'lessons/done.html'

    def get(self, *args, **kwargs):
        user_pk = int(self.request.GET.get('client'))
        lesson_pk = int(self.request.GET.get('lesson'))
        Notification.objects.create(
            lesson_id=lesson_pk,
            to_user_id=user_pk,
            type=Notification.LESSON_DONE,
            lesson_date=datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
        )
        return super().get(*args, **kwargs)
