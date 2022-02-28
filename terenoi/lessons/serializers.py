from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from authapp.models import User, VoxiAccount
from authapp.serializers import UserNameSerializer, VoxiAccountSerializer
from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework
from lessons.services import current_date
from profileapp.models import TeacherSubject, Subject
from profileapp.serializers import SubjectSerializer


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
            for j, h in i.items():
                data += f"Вопрос:{j}\n"
                data += f"Ответ:{h}\n"

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
