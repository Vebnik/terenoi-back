from rest_framework import serializers
from authapp.models import User
from profileapp.models import TeacherSubject, Subject, ReferralPromo


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class SubjectSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ('subject_name',)

    def get_subject_name(self, instance):
        subject = Subject.objects.get(name=instance)
        return subject.name


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
            'time_zone',
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
            'time_zone',
            'phone',
            'bio',
            'education',
            'experience',
            'is_teacher',
            'subjects',
        )

    def get_subjects(self, instance):
        subjects = TeacherSubject.objects.filter(user__pk=instance.pk)
        serializer = SubjectSerializer(subjects, many=True)
        return serializer.data


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralPromo
        fields = ('user_link',)
