import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Sum
from rest_framework import serializers

from authapp.models import User, VoxiAccount
from authapp.serializers import UserNameSerializer, VoxiAccountSerializer
from finance.models import StudentBalance, HistoryPaymentStudent
from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework
from lessons.services import current_date
from profileapp.models import TeacherSubject, Subject
from profileapp.serializers import SubjectSerializer


class UserClassesSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('current_date', 'lessons')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_current_date(self, instance):
        user = self._user()
        date = current_date(user=user, date=instance.get('date'))
        return date

    def get_lessons(self, instance):
        user = self._user()
        if user.is_student:
            date = current_date(user=user, date=instance.get('date'))
            lessons = Lesson.objects.filter(student=user, date__date=date.date())
        else:
            date = current_date(user=user, date=instance.get('date'))
            lessons = Lesson.objects.filter(teacher=user, date__date=date.date())
        serializer = UserLessonsSerializer(lessons, many=True, context={'user': user})
        return serializer.data


class UserLessonsSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    current_date = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    homeworks = serializers.SerializerMethodField()
    record_link = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'pk', 'teacher', 'student', 'topic', 'subject', 'materials', 'deadline', 'homeworks', 'current_date',
            'teacher_status', 'student_status', 'lesson_status', 'record_link', 'rate')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_teacher(self, instance):
        user = User.objects.get(pk=instance.teacher.pk)
        serializer = UserNameSerializer(user)
        return serializer.data

    def get_student(self, instance):
        user = User.objects.get(pk=instance.student.pk)
        serializer = UserNameSerializer(user)
        return serializer.data

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

    def get_homeworks(self, instance):
        homework = LessonHomework.objects.filter(lesson=instance).select_related()
        serializer = LessonHomeworkSerializer(homework, many=True)
        return serializer.data

    def get_rate(self, instance):
        rate = LessonRateHomework.objects.filter(lesson=instance).first()
        serializer = LessonRateHomeworkSerializer(rate)
        return serializer.data

    def get_record_link(self, instance):
        record_data = VoximplantRecordLesson.objects.filter(lesson=instance)
        serializer = RecordSerializer(record_data, many=True)
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
            'weeks', 'weeks_complete_lesson', 'lesson_completed', 'homework_completed', 'balance', 'efficiency',
            'lessons_evaluation', 'next_lesson')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_balance(self, instance):
        balance = HistoryPaymentStudent.objects.filter(student=instance, debit=False, referral=False).aggregate(
            total_count=Sum('lesson_count'))
        return balance['total_count']

    def get_lesson_completed(self, instance):
        lessons = Lesson.objects.filter(student=instance, lesson_status=Lesson.DONE).count()
        return lessons

    def get_homework_completed(self, instance):
        homework = LessonHomework.objects.filter(lesson__student=instance).count()
        return homework

    def get_next_lesson(self, instance):
        lesson = Lesson.objects.filter(student=instance, lesson_status=Lesson.SCHEDULED).order_by('date').first()
        serializer = UserLessonsSerializer(lesson, context={'user': instance})
        return serializer.data

    def get_weeks(self, instance):
        lessons = Lesson.objects.filter(student=instance).dates('date', 'week').count()
        week_list = []
        for i in range(1, lessons + 1):
            week_list.append(str(i))
        return week_list

    def get_weeks_complete_lesson(self, instance):
        lessons = Lesson.objects.filter(student=instance).dates('date', 'week')
        d = datetime.timedelta(days=7)
        complete_lesson_week = []
        complete_lesson = []
        all_lessons = 0
        all_list = []
        for i, j in enumerate(lessons):
            try:
                lesson_user = Lesson.objects.filter(student=instance, lesson_status=Lesson.DONE,
                                                    date__range=[j, lessons[i + 1]]).count()
            except Exception as e:
                new_day = j + d
                lesson_user = Lesson.objects.filter(student=instance, lesson_status=Lesson.DONE,
                                                    date__range=[j, new_day]).count()
            complete_lesson_week.append(str(lesson_user))
            all_lessons += lesson_user
            complete_lesson.append(str(all_lessons))
        all_list.append(complete_lesson_week)
        all_list.append(complete_lesson)

        return all_list

    def get_lessons_evaluation(self, instance):
        subjects = Lesson.objects.filter(student=instance, lesson_status=Lesson.DONE).distinct('subject')
        data = []
        sub_dict = {}
        count_examples = 0
        quality = []
        speaking_list = []
        writing_list = []
        listening_list = []
        grammar_list = []
        for subject in subjects:
            lessons = Lesson.objects.filter(student=instance, subject=subject.subject, lesson_status=Lesson.DONE)
            for lesson in lessons:
                try:
                    new_str = lesson.teacher_rate_comment.split('\n')
                    if lesson.subject.name in 'Математика' or lesson.subject.name in 'Физика':
                        count_examples += int(new_str[1].strip('Ответ:'))
                        quality.append(int(new_str[3].strip('Ответ:')) * 10)
                        average = sum(quality) / len(quality)

                        sub_dict[subject.subject.name] = {
                            new_str[0].strip('Вопрос:'): count_examples,
                            new_str[2].strip('Вопрос:'): average
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
                        sub_dict[subject.subject.name] = {
                            new_str[0].strip('Вопрос:'): average_speaking,
                            new_str[2].strip('Вопрос:'): average_writing,
                            new_str[4].strip('Вопрос:'): average_listening,
                            new_str[6].strip('Вопрос:'): average_grammar
                        }
                        pass
                except Exception:
                    pass
        data.append(sub_dict)
        return data

    def get_efficiency(self, instance):
        subjects = Lesson.objects.filter(student=instance, lesson_status=Lesson.DONE).distinct('subject')
        teacher_eval = []
        count_examples = []
        quality = []
        speaking_list = []
        writing_list = []
        listening_list = []
        grammar_list = []
        data = []
        for subject in subjects:
            lessons = Lesson.objects.filter(student=instance, subject=subject.subject, lesson_status=Lesson.DONE)
            for lesson in lessons:
                try:
                    teacher_eval.append(lesson.teacher_evaluation)
                    new_str = lesson.teacher_rate_comment.split('\n')
                    if lesson.subject.name in 'Математика' or lesson.subject.name in 'Физика':
                        count_examples.append(int(new_str[1].strip('Ответ:')))
                        quality.append(int(new_str[3].strip('Ответ:')))
                        average_quality = sum(quality) / len(quality)
                        average_count_examples = sum(count_examples) / len(count_examples)
                        data.append(average_quality * 10)
                        data.append(average_count_examples * 10)

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
        model = VoximplantRecordLesson
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
        model = Lesson
        fields = ('student_evaluation', 'student_rate_comment', 'teacher_evaluation', 'teacher_rate_comment')


class LessonStudentEvaluationAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('student_evaluation', 'student_rate_comment')


class LessonTeacherEvaluationAddSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('teacher_evaluation', 'answers',)

    def get_answers(self, instance):
        k = self.context.get('request').data.get('answers')
        data = ""
        for i in k:
            data += f"Вопрос:{i['question']}\n"
            data += f"Ответ:{i['answer']}\n"

        lesson = Lesson.objects.get(pk=instance.pk)
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
        fields = ('teacher_status',)


class StudentStatusUpdate(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('student_status',)
