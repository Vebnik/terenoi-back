from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from authapp.models import User, VoxiAccount
from authapp.serializers import UserNameSerializer, VoxiAccountSerializer
from lessons.models import Lesson, LessonMaterials, LessonHomework
from lessons.services import current_date
from profileapp.models import TeacherSubject, Subject
from profileapp.serializers import SubjectSerializer


class UserLessonsSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    current_date = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            'pk', 'teacher', 'student', 'subject', 'current_date',
            'teacher_status', 'student_status', 'lesson_status', 'record')

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


class UserLessonsCreateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        file_fields = kwargs.pop('file_fields', None)
        super().__init__(*args, **kwargs)
        if file_fields:
            field_update_dict = {field: serializers.FileField(required=False, write_only=True) for field in file_fields}
            self.fields.update(**field_update_dict)

    def create(self, validated_data):
        validated_data_copy = validated_data.copy()
        validated_files_materials = []
        validated_files_homework = []
        for key, value in validated_data_copy.items():
            if isinstance(value, InMemoryUploadedFile):
                if 'material' in key:
                    validated_files_materials.append(value)
                    validated_data.pop(key)
                if 'homework' in key:
                    validated_files_homework.append(value)
                    validated_data.pop(key)
        submission_instance = super().create(validated_data)
        for file in validated_files_materials:
            LessonMaterials.objects.create(lesson=submission_instance, material=file)
        for file in validated_files_homework:
            LessonHomework.objects.create(lesson=submission_instance, homework=file)
        return submission_instance

    subject = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    homework = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('pk', 'teacher', 'student', 'subject', 'materials', 'homework', 'date', 'lesson_status')

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
        materials = LessonMaterials.objects.filter(lesson=instance).select_related()
        serializer = LessonMaterialsSerializer(materials, many=True)
        return serializer.data

    def get_homework(self, instance):
        homework = LessonHomework.objects.filter(lesson=instance).select_related()
        serializer = LessonHomeworkSerializer(homework, many=True)
        return serializer.data


class LessonMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonMaterials
        fields = ('material',)


class LessonHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonHomework
        fields = ('homework',)


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
