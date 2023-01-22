import datetime

from dateutil.rrule import rrule, DAILY
from rest_framework import serializers

from authapp.models import User, WebinarRecord, UserStudyLanguage, Group
from authapp.serializers import UserNameSerializer, UserFullNameSerializer, GroupSerializer
from finance.models import TeacherBalance, HistoryPaymentTeacher
from lessons.models import Lesson, LessonMaterials, LessonHomework, LessonRateHomework, \
    Schedule, ScheduleSettings, TeacherWorkHours, TeacherWorkHoursSettings, Feedback
from lessons.services import current_date
from lessons.services.webinar import get_webinar_records
from profileapp.models import Subject, GlobalUserPurpose, TeacherSubject
from profileapp.serializers import SubjectSerializer, UpdateStudentSerializer
from settings.models import WeekDays, DeadlineSettings
from django.conf import settings


class UserClassesSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    all_lessons = serializers.SerializerMethodField()
    done_lessons = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('all_lessons', 'done_lessons', 'subjects', 'current_date', 'lessons')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_all_lessons(self, instance):
        all_lessons = Lesson.objects.filter(group__students=self._user()).exclude(lesson_status=Lesson.CANCEL).exclude(
            lesson_status=Lesson.RESCHEDULED).count()
        return all_lessons

    def get_done_lessons(self, instance):
        done_lessons = Lesson.objects.filter(group__students=self._user(), lesson_status=Lesson.DONE).count()
        return done_lessons

    def get_current_date(self, instance):
        return instance

    def get_lessons(self, instance):
        user = self._user()
        if user.is_student:
            lessons = Lesson.objects.filter(group__students=user, date__date=instance)
        else:
            lessons = Lesson.objects.filter(teacher=user, date__date=instance)
        serializer = UserLessonsSerializer(lessons, many=True, context={'user': user})
        return serializer.data

    def get_subjects(self, instance):
        subject_list = []
        subjects = Lesson.objects.filter(group__students=self._user()).distinct('subject')
        if subjects:
            for sub in subjects:
                subject_list.append(sub.subject)
            serializer = SubjectSerializer(subject_list, many=True)
            return serializer.data
        else:
            return None


class UserLessonsSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    teacher_avatar = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    current_date = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    record_link = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    deadline_days = serializers.SerializerMethodField()
    homeworks = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'pk', 'teacher', 'teacher_avatar', 'students', 'topic', 'subject', 'materials', 'deadline',
            'current_date', 'homeworks',
            'teacher_status', 'student_status', 'lesson_status', 'record_link', 'rate', 'deadline_days')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_homeworks(self, instance):
        homework = LessonHomework.objects.filter(lesson=instance).select_related()
        serializer = LessonHomeworkSerializer(homework, many=True)
        return serializer.data

    def get_teacher(self, instance):
        user = User.objects.get(pk=instance.teacher.pk)
        serializer = UserNameSerializer(user)
        return serializer.data

    def get_students(self, instance):
        users_list = []
        for user in instance.students.all():
            users_list.append(UserNameSerializer(user).data)
        return users_list

    def get_current_date(self, instance):
        user = self._user()
        if not user and self.context.get('user'):
            date = current_date(self.context.get('user'), instance.date)
        else:
            date = current_date(user, instance.date)
        return date

    def get_subject(self, instance):
        serializer = SubjectSerializer(instance.subject)
        return serializer.data

    def get_materials(self, instance):
        materials = LessonMaterials.objects.filter(lesson=instance).select_related()
        serializer = LessonMaterialsSerializer(materials, many=True)
        return serializer.data

    def get_rate(self, instance):
        rate = LessonRateHomework.objects.filter(lesson=instance).first()
        serializer = LessonRateHomeworkSerializer(rate)
        return serializer.data

    def get_record_link(self, instance):
        if not WebinarRecord.objects.filter(webinar__in=list(instance.webinar_set.all())).exists():
            get_webinar_records(instance.webinar_set.all())
        record_data = WebinarRecord.objects.filter(webinar__in=list(instance.webinar_set.all()))
        serializer = RecordSerializer(record_data, many=True)
        return serializer.data

    def get_teacher_avatar(self, instance):
        return instance.teacher.get_avatar()

    def get_deadline_days(self, instance):
        if not instance.deadline:
            days = DeadlineSettings.objects.filter(subject=instance.subject).first()
            if not days:
                return None
            return days.day_count
        elif instance.deadline:
            days = instance.deadline.date() - instance.date.date()
            return days.days
        else:
            return None


class HomepageTeacherSerializer(serializers.ModelSerializer):
    month_lessons = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()
    all_lessons = serializers.SerializerMethodField()
    payment_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('month_lessons', 'all_lessons', 'student_count', 'balance', 'payment_date', 'rate', 'next_lesson')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_month_lessons(self, instance):
        today_month = datetime.datetime.now()
        lesson_month = Lesson.objects.filter(teacher=instance, date__month=today_month.month).count()
        lesson_month_done = Lesson.objects.filter(teacher=instance, date__month=today_month.month,
                                                  lesson_status=Lesson.DONE).count()
        data = {
            'lesson_month_all': lesson_month,
            'lesson_month_done': lesson_month_done
        }
        return data

    def get_all_lessons(self, instance):
        all_lessons = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.DONE).count()
        return all_lessons

    def get_student_count(self, instance):
        student_count = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.SCHEDULED).distinct(
            'group__students').count()
        return student_count

    def get_balance(self, instance):
        balance = TeacherBalance.objects.filter(user=instance).first().money_balance
        return balance if balance else 0

    def get_payment_date(self, instance):
        data = []
        try:
            status = "Выплата"
            date = HistoryPaymentTeacher.objects.filter(teacher=instance).order_by('-payment_date').first()
            curr_date = current_date(user=instance, date=date.payment_date)
            if date.amount > 0:
                status = 'Зачисление'
            data.append({
                'date': curr_date.date(),
                'status': status
            })
            return data
        except Exception:
            return None

    def get_rate(self, instance):
        data = []
        lessons = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.DONE)
        for lesson in lessons:
            try:
                if not lesson.student_evaluation:
                    pass
                else:
                    data.append(lesson.student_evaluation)
            except Exception:
                pass
        if data:
            average = sum(data) / len(data)
            return average
        else:
            return 0

    def get_next_lesson(self, instance):
        lesson_pr = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.PROGRESS).order_by('date').first()
        if not lesson_pr:
            lesson = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.SCHEDULED).order_by('date').first()
            if not lesson:
                lesson_done = Lesson.objects.filter(teacher=instance, lesson_status=Lesson.DONE).order_by(
                    '-date').first()
                serializer = UserLessonsSerializer(lesson_done, context={'user': instance})
                return serializer.data
            serializer = UserLessonsSerializer(lesson, context={'user': instance})
            return serializer.data
        serializer = UserLessonsSerializer(lesson_pr, context={'user': instance})
        return serializer.data


class HomepageStudentSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    lesson_completed = serializers.SerializerMethodField()
    homework_completed = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()
    weeks = serializers.SerializerMethodField()
    weeks_complete_lesson = serializers.SerializerMethodField()
    lessons_evaluation = serializers.SerializerMethodField()
    efficiency = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'weeks',
            'weeks_complete_lesson',
            'lesson_completed',
            'homework_completed',
            'balance',
            'efficiency',
            'lessons_evaluation',
            'next_lesson'
        )

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_balance(self, instance):  # TODO: !!!
        # balance = HistoryPaymentStudent.objects.filter(student=instance, debit=False, referral=False).aggregate(
        #     total_count=Sum('lesson_count'))
        lesson_count = Lesson.objects.filter(group__students=instance).exclude(lesson_status=Lesson.CANCEL).exclude(
            lesson_status=Lesson.RESCHEDULED).count()
        return lesson_count

    def get_lesson_completed(self, instance):
        return Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE).count()

    def get_homework_completed(self, instance):
        return LessonHomework.objects.filter(lesson__group__students=instance).distinct('lesson').count()

    def get_next_lesson(self, instance):
        lesson_pr = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.PROGRESS).order_by('date').first()
        if not lesson_pr:
            lesson = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.SCHEDULED).order_by('date').first()
            if not lesson:
                lesson_done = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE).order_by(
                    '-date').first()
                serializer = UserLessonsSerializer(lesson_done, context={'user': instance})
                return serializer.data
            serializer = UserLessonsSerializer(lesson, context={'user': instance})
            return serializer.data
        serializer = UserLessonsSerializer(lesson_pr, context={'user': instance})
        return serializer.data

    def get_weeks(self, instance):
        lessons = Lesson.objects.filter(group__students=instance).dates('date', 'week').count()
        lessons_all = Lesson.objects.filter(group__students=instance).exclude(lesson_status=Lesson.CANCEL).exclude(
            lesson_status=Lesson.RESCHEDULED).count()
        try:
            k = lessons_all / lessons
            count_lessons_list = []
            week_list = []
            count = 0
            for i in range(0, lessons + 1):
                if i == 0:
                    count_lessons_list.append(str(i))
                else:
                    count += k
                    count_lessons_list.append(str(count))

                week_list.append(str(i))
            data = [week_list, count_lessons_list]
        except Exception:
            return 0
        return data

    def get_weeks_complete_lesson(self, instance):
        lessons = Lesson.objects.filter(group__students=instance).dates('date', 'week')
        date_now = datetime.datetime.now()
        d = datetime.timedelta(days=7)
        count = 0
        flag = False
        for i, lesson in enumerate(lessons):
            if flag:
                break
            date_list = rrule(freq=DAILY, dtstart=lesson, count=7)
            for date in list(date_list):
                if date_now.date() == date.date():
                    count += 1
                    flag = True
                    break
            if not flag:
                count += 1
        complete_lesson_week = []
        complete_lesson = []
        all_lessons = 0
        all_list = []
        for i, lesson in enumerate(lessons):
            if i >= count:
                break
            else:
                try:
                    lesson_user = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE,
                                                        date__range=[lesson, lessons[i + 1]]).count()
                except Exception as e:
                    new_day = lesson + d
                    lesson_user = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE,
                                                        date__range=[lesson, new_day]).count()
                if i == 0:
                    complete_lesson_week.append(str(i))
                    complete_lesson.append(str(i))

                complete_lesson_week.append(str(lesson_user))
                all_lessons += lesson_user
                complete_lesson.append(str(all_lessons))
        all_list.append(complete_lesson_week)
        all_list.append(complete_lesson)

        return all_list

    def get_lessons_evaluation(self, instance):
        subjects = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE).distinct('subject')
        data = []
        sub_dict = {}
        count_examples = 0
        quality = []
        speaking_list = []
        writing_list = []
        listening_list = []
        grammar_list = []
        for subject in subjects:
            lessons = Lesson.objects.filter(group__students=instance, subject=subject.subject, lesson_status=Lesson.DONE)
            for lesson in lessons:
                try:
                    new_str = lesson.teacher_rate_comment.split('\n')
                    if lesson.subject.name in 'Математика' or lesson.subject.name in 'Физика':
                        count_examples += int(new_str[1].strip('Ответ:'))
                        quality.append(int(new_str[3].strip('Ответ:')) * 10)
                        average = sum(quality) / len(quality)

                        sub_dict[subject.subject.name] = {
                            'title': new_str[2].strip('Вопрос:'),
                            'percent': average,
                            'count_issues': count_examples
                        }
                    else:
                        speaking_list.append(int(new_str[1].strip('Ответ:')) * 10)
                        writing_list.append(int(new_str[3].strip('Ответ:')) * 10)
                        listening_list.append(int(new_str[5].strip('Ответ:')) * 10)
                        grammar_list.append(int(new_str[7].strip('Ответ:')) * 10)
                        average_speaking = sum(speaking_list) / len(speaking_list)
                        average_writing = sum(writing_list) / len(writing_list)
                        average_listening = sum(listening_list) / len(listening_list)
                        average_grammar = sum(grammar_list) / len(grammar_list)
                        sub_dict[subject.subject.name] = [
                            {
                                'title': new_str[0].strip('Вопрос:'),
                                'percent': average_speaking
                            },
                            {
                                'title': new_str[2].strip('Вопрос:'),
                                'percent': average_writing
                            },
                            {
                                'title': new_str[4].strip('Вопрос:'),
                                'percent': average_listening
                            },
                            {
                                'title': new_str[6].strip('Вопрос:'),
                                'percent': average_grammar
                            },

                            # new_str[0].strip('Вопрос:'): average_speaking,
                            # new_str[2].strip('Вопрос:'): average_writing,
                            # new_str[4].strip('Вопрос:'): average_listening,
                            # new_str[6].strip('Вопрос:'): average_grammar
                        ]
                        pass
                except Exception:
                    pass
        for i in sub_dict.keys():
            data.append({
                'subject': i,
                'items': sub_dict[i]
            })
        return data

    def get_efficiency(self, instance):
        subjects = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.DONE).distinct('subject')
        teacher_eval = []
        quality = []
        speaking_list = []
        writing_list = []
        listening_list = []
        grammar_list = []
        data = []
        for subject in subjects:
            lessons = Lesson.objects.filter(group__students=instance, subject=subject.subject, lesson_status=Lesson.DONE)
            for lesson in lessons:
                try:
                    if lesson.teacher_evaluation:
                        teacher_eval.append(lesson.teacher_evaluation)
                    new_str = lesson.teacher_rate_comment.split('\n')
                    if lesson.subject.name in 'Математика' or lesson.subject.name in 'Физика':
                        quality.append(int(new_str[3].strip('Ответ:')))
                        average_quality = sum(quality) / len(quality)
                        data.append(average_quality * 10)
                    else:
                        speaking_list.append(int(new_str[1].strip('Ответ:')))
                        writing_list.append(int(new_str[3].strip('Ответ:')))
                        listening_list.append(int(new_str[5].strip('Ответ:')))
                        grammar_list.append(int(new_str[7].strip('Ответ:')))
                        average_speaking = sum(speaking_list) / len(speaking_list)
                        average_writing = sum(writing_list) / len(writing_list)
                        average_listening = sum(listening_list) / len(listening_list)
                        average_grammar = sum(grammar_list) / len(grammar_list)
                        data.append(average_speaking * 10)
                        data.append(average_writing * 10)
                        data.append(average_listening * 10)
                        data.append(average_grammar * 10)
                        pass
                except Exception:
                    pass
        try:

            teacher_eval_average = sum(teacher_eval) / len(teacher_eval)
            data.append(teacher_eval_average * 10)
            avg = sum(data) / len(data)
        except Exception:
            return None
        return round(avg, 2)


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarRecord
        fields = ('record',)


class LessonMaterialsDetail(serializers.ModelSerializer):
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('materials',)

    def get_materials(self, instance):
        materials = LessonMaterials.objects.filter(lesson=instance).select_related()
        serializer = LessonMaterialsSerializer(materials, many=True)
        return serializer.data


class LessonRateHomeworkDetail(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('rate',)

    def get_rate(self, instance):
        rate = LessonRateHomework.objects.filter(lesson=instance).first()
        serializer = LessonRateHomeworkSerializer(rate)
        return serializer.data


class LessonTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('lesson_status', 'transfer_date', 'transfer_comment')


class LessonRateHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRateHomework
        fields = ('rate', 'rate_comment')


class LessonHomeworksDetail(serializers.ModelSerializer):
    homeworks = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('homeworks',)

    def get_homeworks(self, instance):
        homework = LessonHomework.objects.filter(lesson=instance).select_related()
        serializer = LessonHomeworkSerializer(homework, many=True)
        return serializer.data


class UserLessonsCreateSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    homework = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('pk', 'teacher', 'topic', 'student', 'subject', 'materials', 'homework', 'date', 'lesson_status')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_date(self, instance):
        user = self._user()
        date = current_date(user, instance.date)
        return date

    def get_subject(self, instance):
        sub = self.context.get('request').data.get('subject')
        if sub:
            subject = Subject.objects.get(name=sub)
            lesson = Lesson.objects.get(pk=instance.pk)
            lesson.subject = subject
            lesson.save()
        serializer = SubjectSerializer(sub)
        return serializer.data

    def get_materials(self, instance):
        request = self.context.get('request', None)
        if request.FILES.getlist('material'):
            for material in request.FILES.getlist('material'):
                LessonMaterials.objects.create(lesson=instance, material=material)
        materials = LessonMaterials.objects.filter(lesson=instance).select_related()
        serializer = LessonMaterialsSerializer(materials, many=True)
        return serializer.data

    def get_homework(self, instance):
        request = self.context.get('request', None)
        if request.FILES.getlist('homework'):
            for homework in request.FILES.getlist('homework'):
                LessonHomework.objects.create(lesson=instance, homework=homework)
        homework = LessonHomework.objects.filter(lesson=instance).select_related()
        serializer = LessonHomeworkSerializer(homework, many=True)
        return serializer.data


class TeacherScheduleCreateSerializer(serializers.ModelSerializer):
    daysOfWeek = serializers.SerializerMethodField()
    startTime = serializers.SerializerMethodField()
    endTime = serializers.SerializerMethodField()

    class Meta:
        model = TeacherWorkHoursSettings
        fields = ('daysOfWeek', 'startTime', 'endTime')

    def get_daysOfWeek(self, instance):
        data = [instance.weekday.american_number]
        return data

    def get_startTime(self, instance):
        return instance.start_time

    def get_endTime(self, instance):
        return instance.end_time


class TeacherRecruitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_recruiting',)


class TeacherScheduleDetailSerializer(serializers.ModelSerializer):
    daysOfWeek = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()

    class Meta:
        model = TeacherWorkHoursSettings
        fields = ('daysOfWeek', 'periods')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_daysOfWeek(self, instance):
        data = [instance.weekday.american_number]
        return data

    def get_periods(self, instance):
        data = []
        if not self._user():
            user = self.context.get('teacher')
        else:
            user = self._user()
        th_work = TeacherWorkHours.objects.filter(teacher=user).first()
        weekday = WeekDays.objects.filter(american_number=instance.weekday.american_number).first()
        queryset = TeacherWorkHoursSettings.objects.filter(teacher_work_hours=th_work, weekday=weekday)
        for qr in queryset:
            data.append({
                'startTime': qr.start_time,
                'endTime': qr.end_time
            })
        return data


class TeacherScheduleNoneDetailSerializer(serializers.ModelSerializer):
    daysOfWeek = serializers.SerializerMethodField()
    periods = serializers.SerializerMethodField()

    class Meta:
        model = WeekDays
        fields = ('daysOfWeek', 'periods')

    def get_daysOfWeek(self, instance):
        data = [instance.american_number]
        return data

    def get_periods(self, instance):
        data = [{
            'startTime': '',
            'endTime': ''
        }]
        return data


class LessonMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterials
        fields = ('material', 'text_material')


class LessonHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHomework
        fields = ('homework', 'text_homework')


class LessonEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('student_evaluation', 'student_rate_comment', 'teacher_evaluation', 'teacher_rate_comment')


class LessonStudentEvaluationAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('student_evaluation', 'student_rate_comment')


class LessonTeacherEvaluationAddSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ('teacher_evaluation', 'answers',)

    def get_answers(self, instance):
        k = self.context.get('request').data.get('answers')
        data = ""
        for i in k:
            data += f"Вопрос:{i['question']}\n"
            data += f"Ответ:{i['answer']}\n"

        lesson = Lesson.objects.get(pk=instance.lesson.pk)
        lesson.teacher_rate_comment = data
        lesson.save()
        return lesson.teacher_rate_comment


class LessonEvaluationQuestionsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('questions',)

    def get_questions(self, instance):
        if not instance.teacher_rate_comment:
            return None
        else:
            questions_list = instance.teacher_rate_comment.split(',')
            return questions_list


class VoxiTeacherInfoSerializer(serializers.ModelSerializer):
    voxi_account = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('teacher_status', 'voxi_account')

    def get_voxi_account(self, instance):
        voxi_acc = VoxiAccount.objects.get(user=instance.teacher)
        serializer = VoxiAccountSerializer(voxi_acc)
        return serializer.data


class VoxiStudentInfoSerializer(serializers.ModelSerializer):
    voxi_account = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('student_status', 'voxi_account')

    def get_voxi_account(self, instance):
        voxi_acc = VoxiAccount.objects.get(user=instance.student)
        serializer = VoxiAccountSerializer(voxi_acc)
        return serializer.data


class TeacherStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('teacher_status', 'teacher_entry_date')


class StudentStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('student_status', 'student_entry_date')


class StudentsTeacherSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk', 'avatar', 'username', 'first_name', 'last_name', 'english_level', 'student_class', 'lessons_count',
            'start_date', 'end_date')

    def get_lessons_count(self, instance):
        lessons_count = Lesson.objects.filter(group__students=instance, lesson_status=Lesson.SCHEDULED,
                                              subject=self.context.get('subject')).count()
        return lessons_count

    def get_avatar(self, instance):
        return instance.get_avatar()

    def get_start_date(self, instance):
        start_date = Lesson.objects.filter(group__students=instance, subject=self.context.get('subject'),
                                           teacher=self.context.get('teacher')).order_by('date').first()
        if start_date:
            cur_date = current_date(user=self.context.get('teacher'), date=start_date.date)
            return cur_date.date()
        return None

    def get_end_date(self, instance):
        end_date = Lesson.objects.filter(group__students=instance, subject=self.context.get('subject'),
                                         teacher=self.context.get('teacher'), lesson_status=Lesson.SCHEDULED)
        if not end_date:
            end_date_inactive = Lesson.objects.filter(group__students=instance, subject=self.context.get('subject'),
                                                      teacher=self.context.get('teacher'),
                                                      lesson_status=Lesson.DONE).order_by('-date').first()
            if end_date_inactive:
                cur_date = current_date(user=self.context.get('teacher'), date=end_date_inactive.date)
                return cur_date.date()
        return None


class StudentsActiveTeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk', 'avatar', 'first_name', 'last_name', 'student_class', 'subjects')

    def get_avatar(self, instance):
        return instance.get_avatar()

    def get_subjects(self, instance):
        data = []
        teacher = self.context.get('teacher')
        subjects = Lesson.objects.filter(student=instance, teacher=teacher).distinct('subject')
        for sub in subjects:
            data.append(sub.subject.name)
        return data


class StudentsSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('students',)

    def get_students(self, instance):
        data = []
        subjects = Lesson.objects.filter(teacher=instance).distinct('subject')
        for subject in subjects:
            inactive_list = []
            active_list = []
            all_lessons = Lesson.objects.filter(teacher=instance, subject=subject.subject)
            for lesson in all_lessons:
                for student in lesson.students.all():
                    inactive = Lesson.objects.filter(teacher=instance, subject=subject.subject, group__students=student,
                                                     lesson_status=Lesson.SCHEDULED).exists()
                    if not inactive and student not in inactive_list:
                        inactive_list.append(student)
                    else:
                        if student not in active_list:
                            active_list.append(student)

            serializer_active = StudentsTeacherSerializer(active_list, many=True,
                                                          context={'subject': subject.subject, 'teacher': instance})
            serializer_inactive = StudentsTeacherSerializer(inactive_list, many=True,
                                                            context={'subject': subject.subject, 'teacher': instance})
            data.append({
                'subject': subject.subject.name,
                'active_students': serializer_active.data,
                'inactive_students': serializer_inactive.data
            })
        return data


class StudentsActiveSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('students',)

    def get_students(self, instance):
        data = []
        all_students = Lesson.objects.filter(teacher=instance).distinct('student')
        active_list = []
        for student in all_students:
            inactive = Lesson.objects.filter(teacher=instance, student=student.student,
                                             lesson_status=Lesson.SCHEDULED).first()
            if inactive:
                active_list.append(student.student)

        serializer_active = StudentsActiveTeacherSerializer(active_list, many=True, context={'teacher': instance})

        # subjects = Lesson.objects.filter(teacher=instance).distinct('subject')
        # for subject in subjects:
        #     print(subject.subject.name)
        #     inactive_list = []
        #     active_list = []
        #     all_students = Lesson.objects.filter(teacher=instance, subject=subject.subject).distinct('student')
        #     for student in all_students:
        #         inactive = Lesson.objects.filter(teacher=instance, subject=subject.subject, student=student.student,
        #                                          lesson_status=Lesson.SCHEDULED).first()
        #         if not inactive:
        #            pass
        #         else:
        #             active_list.append(student.student)
        #
        #     serializer_active = StudentsTeacherSerializer(active_list, many=True,
        #                                                   context={'subject': subject.subject, 'teacher': instance})
        #     serializer_inactive = StudentsTeacherSerializer(inactive_list, many=True,
        #                                                     context={'subject': subject.subject, 'teacher': instance})
        #     data.append({
        #         'subject': subject.subject.name,
        #         'active_students': serializer_active.data,
        #     })
        return serializer_active.data


class StudentDetailSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    student_classes = serializers.SerializerMethodField()
    student_schedule = serializers.SerializerMethodField()
    lesson_plan = serializers.SerializerMethodField()
    student_homework = serializers.SerializerMethodField()
    student_lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'student', 'student_lesson_count', 'student_classes', 'lesson_plan', 'student_schedule', 'student_homework')

    def _student(self):
        student = User.objects.filter(pk=self.context.get('pk')).first()
        return student

    def get_student(self, instance):
        serializer = UpdateStudentSerializer(self._student())
        return serializer.data

    def get_student_lesson_count(self, instance):
        try:
            data = []
            if self.context.get('params').get('subject'):
                subject = Subject.objects.filter(name=self.context.get('params').get('subject')).first()
                all_lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                    subject__name=self.context.get('params').get('subject')).exclude(
                    lesson_status=Lesson.CANCEL).exclude(
                    lesson_status=Lesson.RESCHEDULED).count()
                done_lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                     lesson_status=Lesson.DONE,
                                                     subject__name=self.context.get('params').get('subject')).count()
                active_lesson = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                      lesson_status=Lesson.SCHEDULED,
                                                      subject__name=self.context.get('params').get('subject')).count()
                data.append({
                    'subject': subject.name,
                    'all_lessons': all_lessons,
                    'done_lessons': done_lessons,
                    'active_lesson': active_lesson
                })
        except Exception:
            return None
        return data

    def get_student_classes(self, instance):
        data = []
        if self.context.get('params').get('subject'):
            subject = Subject.objects.filter(name=self.context.get('params').get('subject')).first()
            data_classes = []
            lessons_list = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                 subject__name=self.context.get('params').get('subject')).values(
                'date').order_by('date')
            date_list = []
            for item in lessons_list:
                date = current_date(user=instance, date=item.get('date')).date()
                if date in date_list:
                    pass
                else:
                    date_list.append(current_date(user=instance, date=item.get('date')).date())

            for date in date_list:
                lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                subject__name=self.context.get('params').get('subject'),
                                                date__date=date)
                serializer = UserLessonsSerializer(lessons, many=True, context={'user': self._student()})
                data_classes.append({
                    'current_date': date,
                    'classes': serializer.data
                })
            data.append({
                'subject': subject.name,
                'classes_data': data_classes
            })
        return data

    def get_student_schedule(self, instance):
        data = []
        if self.context.get('params').get('subject'):
            subject = Subject.objects.filter(name=self.context.get('params').get('subject')).first()
            time = None
            data_wekday = []
            shedules = Schedule.objects.filter(group__students=self._student(), teacher=instance,
                                               subject__name=self.context.get('params').get('subject'),
                                               is_completed=False)
            if shedules:
                for sh in shedules:
                    for weekday in sh.weekday.all():
                        data_wekday.append(weekday.name)
                    sh_settings = ScheduleSettings.objects.filter(shedule=sh).order_by('-last_lesson').first()
                    curr_date = current_date(user=instance, date=sh_settings.last_lesson)
                    time = curr_date.time()

            data.append({
                'subject': subject.name,
                'time': time,
                'weekday': data_wekday
            })

        return data

    def get_lesson_plan(self, instance):
        data = []
        if self.context.get('params').get('subject'):
            subject = Subject.objects.filter(name=self.context.get('params').get('subject')).first()
            purpose = None
            data_lesson = []
            student_purpose = GlobalUserPurpose.objects.filter(user=self._student(),
                                                               subject__name=self.context.get('params').get(
                                                                   'subject')).first()
            print(student_purpose)
            if student_purpose:
                purpose = student_purpose.purpose.name
            lessons = Lesson.objects.filter(group__students=self._student(),
                                            subject__name=self.context.get('params').get('subject'),
                                            schedule__isnull=False).exclude(
                lesson_status=Lesson.CANCEL).exclude(lesson_status=Lesson.RESCHEDULED).order_by('date')
            for les in lessons:
                data_lesson.append({
                    'lesson_id': les.pk,
                    'lesson_count': les.lesson_number,
                    'topic': les.topic
                })

            data.append({
                'subject': subject.name,
                'purpose': purpose,
                'lesson_topic': data_lesson
            })
        return data

    def get_student_homework(self, instance):
        data = []
        lessons = None
        if self.context.get('params').get('subject'):
            subject = Subject.objects.filter(name=self.context.get('params').get('subject')).first()
            data_lesson = []
            serializer_homework = None
            serializer_rate = None
            try:
                if self.context.get('params').get('filter') and self.context.get('params').get('check'):
                    if self.context.get('params').get('filter') == 'new':
                        lessons_lst = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                            subject__name=self.context.get('params').get('subject'),
                                                            lesson_status=Lesson.DONE).order_by('-date')
                        if self.context.get('params').get('check') == 'true':
                            for lsn in lessons_lst:
                                rate = LessonRateHomework.objects.filter(lesson=lsn)
                                if rate:
                                    lessons.append(lsn)
                        else:
                            for lsn in lessons_lst:
                                rate = LessonRateHomework.objects.filter(lesson=lsn)
                                if not rate:
                                    lessons.append(lsn)
                    else:
                        lessons_lst = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                            subject__name=self.context.get('params').get('subject'),
                                                            lesson_status=Lesson.DONE).order_by('date')
                        if self.context.get('params').get('check') == 'true':
                            for lsn in lessons_lst:
                                rate = LessonRateHomework.objects.filter(lesson=lsn)
                                if rate:
                                    lessons.append(lsn)
                        else:
                            for lsn in lessons_lst:
                                rate = LessonRateHomework.objects.filter(lesson=lsn)
                                if not rate:
                                    lessons.append(lsn)
                elif self.context.get('params').get('check'):
                    lessons_lst = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                        subject__name=self.context.get('params').get('subject'),
                                                        lesson_status=Lesson.DONE)
                    if self.context.get('params').get('check') == 'true':
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if rate:
                                lessons.append(lsn)
                    else:
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if not rate:
                                lessons.append(lsn)
                elif self.context.get('params').get('filter'):
                    if self.context.get('params').get('filter') == 'new':
                        lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                        subject__name=self.context.get('params').get('subject'),
                                                        lesson_status=Lesson.DONE).order_by('-date')
                    else:
                        lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                        subject__name=self.context.get('params').get('subject'),
                                                        lesson_status=Lesson.DONE).order_by('date')
            except Exception:
                lessons = Lesson.objects.filter(group__students=self._student(), teacher=instance,
                                                subject__name=self.context.get('params').get('subject'),
                                                lesson_status=Lesson.DONE)
            if lessons:
                for les in lessons:
                    check = False
                    homeworks = LessonHomework.objects.filter(lesson=les)
                    serializer_homework = LessonHomeworkSerializer(homeworks, many=True)
                    if serializer_homework.data:
                        rate = LessonRateHomework.objects.filter(lesson=les)
                        serializer_rate = LessonRateHomeworkSerializer(rate, many=True)
                        if serializer_rate.data:
                            check = True
                        data_lesson.append({
                            'lesson_id': les.pk,
                            'lesson_count': les.lesson_number,
                            'topic': les.topic,
                            'homework': serializer_homework.data,
                            'rate': serializer_rate.data,
                            'deadline': les.deadline,
                            'check': check
                        })
            data.append({
                'subject': subject.name,
                'homework_data': data_lesson
            })
        return data


class StudentTeacherClassesSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('current_date', 'lessons')

    def get_current_date(self, instance):
        return instance


class HomeworksSerializer(serializers.ModelSerializer):
    homeworks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('homeworks',)

    def get_homeworks(self, instance):
        data_lesson = []
        lessons_list = None
        serializer_homework = None
        serializer_rate = None
        try:
            if self.context.get('params').get('filter') and self.context.get('params').get(
                    'check') and self.context.get('params').get('subject'):
                if self.context.get('params').get('filter') == 'new':
                    lessons_lst = Lesson.objects.filter(teacher=instance,
                                                        subject__name=self.context.get('params').get('subject'),
                                                        lesson_status=Lesson.DONE).order_by('-date')
                    if self.context.get('params').get('check') == 'true':
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if rate:
                                lessons_list.append(lsn)
                    else:
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if not rate:
                                lessons_list.append(lsn)
                else:
                    lessons_lst = Lesson.objects.filter(teacher=instance,
                                                        subject__name=self.context.get('params').get('subject'),
                                                        lesson_status=Lesson.DONE).order_by('date')
                    if self.context.get('params').get('check') == 'true':
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if rate:
                                lessons_list.append(lsn)
                    else:
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if not rate:
                                lessons_list.append(lsn)
            elif self.context.get('params').get('check') and self.context.get('params').get('subject'):
                lessons_lst = Lesson.objects.filter(teacher=instance,
                                                    subject__name=self.context.get('params').get('subject'),
                                                    lesson_status=Lesson.DONE)
                if self.context.get('params').get('check') == 'true':
                    for lsn in lessons_lst:
                        rate = LessonRateHomework.objects.filter(lesson=lsn)
                        if rate:
                            lessons_list.append(lsn)
                else:
                    for lsn in lessons_lst:
                        rate = LessonRateHomework.objects.filter(lesson=lsn)
                        if not rate:
                            lessons_list.append(lsn)
            elif self.context.get('params').get('check') and self.context.get('params').get('filter'):
                if self.context.get('params').get('filter') == 'new':
                    lessons_lst = Lesson.objects.filter(teacher=instance,
                                                        lesson_status=Lesson.DONE).order_by('-date')
                    if self.context.get('params').get('check') == 'true':
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if rate:
                                lessons_list.append(lsn)
                    else:
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if not rate:
                                lessons_list.append(lsn)
                else:
                    lessons_lst = Lesson.objects.filter(teacher=instance,
                                                        lesson_status=Lesson.DONE).order_by('date')
                    if self.context.get('params').get('check') == 'true':
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if rate:
                                lessons_list.append(lsn)
                    else:
                        for lsn in lessons_lst:
                            rate = LessonRateHomework.objects.filter(lesson=lsn)
                            if not rate:
                                lessons_list.append(lsn)
            elif self.context.get('params').get('filter') and self.context.get('params').get('subject'):
                if self.context.get('params').get('filter') == 'new':
                    lessons_list = Lesson.objects.filter(teacher=instance,
                                                         subject__name=self.context.get('params').get('subject'),
                                                         lesson_status=Lesson.DONE).order_by('-date')
                else:
                    lessons_list = Lesson.objects.filter(teacher=instance,
                                                         subject__name=self.context.get('params').get('subject'),
                                                         lesson_status=Lesson.DONE).order_by('date')

            elif self.context.get('params').get('check'):
                lessons_lst = Lesson.objects.filter(teacher=instance,
                                                    lesson_status=Lesson.DONE)
                if self.context.get('params').get('check') == 'true':
                    for lsn in lessons_lst:
                        rate = LessonRateHomework.objects.filter(lesson=lsn)
                        if rate:
                            lessons_list.append(lsn)
                else:
                    for lsn in lessons_lst:
                        rate = LessonRateHomework.objects.filter(lesson=lsn)
                        if not rate:
                            lessons_list.append(lsn)
            elif self.context.get('params').get('filter'):
                if self.context.get('params').get('filter') == 'new':
                    lessons_list = Lesson.objects.filter(teacher=instance,
                                                         lesson_status=Lesson.DONE).order_by('-date')
                else:
                    lessons_list = Lesson.objects.filter(teacher=instance,
                                                         lesson_status=Lesson.DONE).order_by('date')
            elif self.context.get('params').get('subject'):
                lessons_list = Lesson.objects.filter(teacher=instance,
                                                     subject__name=self.context.get('params').get('subject'),
                                                     lesson_status=Lesson.DONE)
        except Exception:
            lessons_list = Lesson.objects.filter(teacher=instance,
                                                 lesson_status=Lesson.DONE)
        if lessons_list:
            for les in lessons_list:
                student_data = []
                check = False
                homeworks = LessonHomework.objects.filter(lesson=les)
                serializer_homework = LessonHomeworkSerializer(homeworks, many=True)
                for student_item in les.students.all():
                    serializer_student = UserNameSerializer(student_item)
                    if serializer_homework.data:
                        rate = LessonRateHomework.objects.filter(lesson=les)
                        serializer_rate = LessonRateHomeworkSerializer(rate, many=True)
                        if serializer_rate.data:
                            check = True
                        data_lesson.append({
                            'student': serializer_student.data,
                            'lesson_id': les.pk,
                            'lesson_count': les.lesson_number,
                            'topic': les.topic,
                            'homework': serializer_homework.data,
                            'rate': serializer_rate.data,
                            'deadline': les.deadline,
                            'check': check
                        })

        return data_lesson


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('topic',)


class TeacherSubjectSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('languages',)

    def get_languages(self, instance):
        languages = TeacherSubject.objects.filter(user=instance).all()
        if languages:
            names = [lang_names.subject.name for lang_names in languages.all()]
            return names
        raise serializers.ValidationError('Languages not found')


class TeacherStudentsListSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('students',)

    def get_students(self, instance):
        groups = Group.objects.filter(teacher=instance).all()
        if groups:
            students_group = groups.values('students').distinct('students')
            students_list = [User.objects.get(pk=student.get('students')) for student in students_group]
            serializer = UserFullNameSerializer(students_list, many=True)
            return serializer.data
        raise serializers.ValidationError('Students not found')


class FastLessonCreateSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('pk', 'teacher', 'topic', 'date', 'group', 'subject')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_date(self, instance):
        import pytz
        current_timezone = pytz.timezone(pytz.UTC)
        return instance.date.astimezone(current_timezone)

    def get_group(self, instance):
        import pytz
        user = self._user()
        student_list = [User.objects.get(pk=item.get('pk')) for item in self.context.get('request').data.get('group')]
        title = f'Fast Lesson with teacher {user.username}, lesson №{instance.pk}'
        descr = f'Fast Lesson with teacher {user.username}'
        fast_group = Group.objects.create(title=title, description=descr, teacher=user, create_status=Group.CREATE_FAST)
        for student in student_list:
            fast_group.students.add(student)
        fast_group.save()
        lesson = Lesson.objects.get(pk=instance.pk)
        lesson.group = fast_group
        lesson.date += datetime.datetime.now(pytz.timezone(settings.TIME_ZONE)).utcoffset()
        lesson.save()
        serializer = GroupSerializer(lesson.group)
        return serializer.data

    def get_subject(self, instance):
        sub = self.context.get('request').data.get('subject')
        if sub:
            subject = Subject.objects.get(name=sub)
            lesson = Lesson.objects.get(pk=instance.pk)
            lesson.subject = subject
            lesson.save()
        serializer = SubjectSerializer(sub)
        return serializer.data
