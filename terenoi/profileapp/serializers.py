from rest_framework import serializers
from authapp.models import User
from profileapp.models import Subject


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject',)


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'phone',
            'bio',
            'is_student'
        )


class UpdateTeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'phone',
            'bio',
            'education',
            'experience',
            'is_teacher',
            'subjects',
        )

    def get_subjects(self, instance):
        subjects = Subject.objects.filter(user__pk=instance.pk)
        serializer = SubjectSerializer(subjects, many=True)
        return serializer.data
