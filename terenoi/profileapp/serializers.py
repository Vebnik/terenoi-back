from rest_framework import serializers
from authapp.models import User
from lessons.models import Lesson
from profileapp.models import TeacherSubject, Subject, ReferralPromo, UserParents, GlobalUserPurpose, LanguageInterface, \
    Interests, UserInterest
from settings.models import UserCity
from settings.serializers import CityUserSerializer


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
    city = serializers.SerializerMethodField()
    parents_data = serializers.SerializerMethodField()
    purposes = serializers.SerializerMethodField()
    language_interface = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'birth_date',
            'city',
            'parents_data',
            'purposes',
            'interests',
            'language',
            'time_zone',
            'phone',
            'bio',
            'language_interface',
            'is_student'
        )

    def get_city(self, instance):
        city = UserCity.objects.filter(user=instance).first()
        serializer = CityUserSerializer(city)
        return serializer.data

    def get_parents_data(self, instance):
        parents = UserParents.objects.filter(user=instance)
        serializer = UserParentsSerializer(parents, many=True)
        return serializer.data

    def get_purposes(self, instance):
        purposes = GlobalUserPurpose.objects.filter(user=instance)
        serializer = GlobalUserPurposeSerializer(purposes, many=True, context={'user': instance})
        if not serializer.data:
            data = []
            lesson_subjects = Lesson.objects.filter(student=instance).distinct('subject')
            for lesson in lesson_subjects:
                lesson_count_all = Lesson.objects.filter(student=instance,
                                                         subject__name=lesson.subject.name).exclude(
                    lesson_status=Lesson.CANCEL).exclude(lesson_status=Lesson.RESCHEDULED).count()
                lesson_count_done = Lesson.objects.filter(student=instance,
                                                          subject__name=lesson.subject.name,
                                                          lesson_status=Lesson.DONE).count()
                data.append(
                    {'subject': lesson.subject.name,
                     'lesson_count_all': lesson_count_all,
                     'lesson_count_done': lesson_count_done
                     }
                )
            return data
        return serializer.data

    def get_language_interface(self, instance):
        language_interface = LanguageInterface.objects.filter(user=instance).first()
        serializer = LanguageInterfaceSerializer(language_interface)
        return serializer.data

    def get_interests(self, instance):
        interests = Interests.objects.all()
        serializer = InterestsSerializer(interests, many=True, context={'user': instance})
        return serializer.data


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
            'city',
            'time_zone',
            'phone',
            'gender',
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

    def get_city(self, instance):
        city = UserCity.objects.filter(user=instance).first()
        serializer = CityUserSerializer(city)
        return serializer.data


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralPromo
        fields = ('user_link',)


class UserParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserParents
        fields = ('pk', 'full_name', 'parent_phone', 'parent_email')


class GlobalUserPurposeSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()
    lesson_count_all = serializers.SerializerMethodField()
    lesson_count_done = serializers.SerializerMethodField()

    class Meta:
        model = GlobalUserPurpose
        fields = ('subject_name', 'purpose', 'lesson_count_all', 'lesson_count_done')

    def get_subject_name(self, instance):
        subject = Subject.objects.filter(name=instance.subject.name).first()
        return subject.name

    def get_lesson_count_all(self, instance):
        lesson_count = Lesson.objects.filter(student=self.context.get('user'),
                                             subject__name=instance.subject.name).exclude(
            lesson_status=Lesson.CANCEL).exclude(lesson_status=Lesson.RESCHEDULED).count()
        return lesson_count

    def get_lesson_count_done(self, instance):
        lesson_count = Lesson.objects.filter(student=self.context.get('user'),
                                             subject__name=instance.subject.name, lesson_status=Lesson.DONE).count()
        return lesson_count


class LanguageInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageInterface
        fields = ('interface_language',)


class InterestsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Interests
        fields = ('name', 'status')

    def get_status(self, instance):
        user_interest = UserInterest.objects.filter(user=self.context.get('user')).first()
        if not user_interest:
            return False
        elif instance in user_interest.interests.all():
            return True
        else:
            return False
