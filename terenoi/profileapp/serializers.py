import base64
import os
import re
from io import BytesIO

from PIL import Image
from django.conf import settings
from rest_framework import serializers
from authapp.models import User, UserStudyLanguage, StudyLanguage
from authapp.serializers import StudyLanguageSerializer, DataManagerSerializer
from lessons.models import Lesson
from profileapp.models import TeacherSubject, Subject, ReferralPromo, UserParents, GlobalUserPurpose, LanguageInterface, \
    Interests, UserInterest, AgeLearning, MathSpecializations, TeacherAgeLearning, TeacherMathSpecializations, \
    EnglishSpecializations, TeacherEnglishSpecializations, EnglishLevel, TeacherEnglishLevel, ManagerToUser
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
    language = serializers.SerializerMethodField()

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

    def get_language(self, instance):
        langs = StudyLanguage.objects.all()
        serializer = StudyLanguageSerializer(langs, many=True, context={'user': instance})
        return serializer.data


class UpdateUserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',)

    def to_internal_value(self, data):
        if 'avatar' in data:
            image_path = f'{settings.MEDIA_ROOT}/user_avatar/{self.instance.username}-avatar.jpeg'
            image_name = f'{self.instance.username}-avatar.jpeg'
            if data['avatar']:
                base64_img = data['avatar']
                byte_data = base64.b64decode(base64_img)
                image_data = BytesIO(byte_data)
                if self.instance.avatar:
                    self.instance.avatar.delete()
                self.instance.avatar.save(image_name, image_data, save=True)
            else:
                os.remove(image_path)
        return super(UpdateUserAvatarSerializer, self).to_internal_value(data)


class UpdateTeacherSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    math_special = serializers.SerializerMethodField()
    english_special = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

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
            'phone',
            'gender',
            'language',
            'age',
            'math_special',
            'english_special',
            'level',
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

    def get_age(self, instance):
        ages = AgeLearning.objects.all()
        serializer = AgeLearningSerializer(ages, many=True, context={'user': instance})
        return serializer.data

    def get_math_special(self, instance):
        specials = MathSpecializations.objects.all()
        serializer = MathSpecializationsSerializer(specials, many=True, context={'user': instance})
        return serializer.data

    def get_english_special(self, instance):
        specials = EnglishSpecializations.objects.all()
        serializer = EnglishSpecializationsSerializer(specials, many=True, context={'user': instance})
        return serializer.data

    def get_level(self, instance):
        specials = EnglishLevel.objects.all()
        serializer = EnglishLevelSerializer(specials, many=True, context={'user': instance})
        return serializer.data

    def get_language(self, instance):
        langs = StudyLanguage.objects.all()
        serializer = StudyLanguageSerializer(langs, many=True, context={'user': instance})
        return serializer.data


class EnglishLevelSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = EnglishLevel
        fields = ('name', 'status')

    def get_status(self, instance):
        user_level = TeacherEnglishLevel.objects.filter(user=self.context.get('user')).first()
        if not user_level:
            return False
        elif instance in user_level.level.all():
            return True
        else:
            return False


class EnglishSpecializationsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = EnglishSpecializations
        fields = ('name', 'status')

    def get_status(self, instance):
        user_english = TeacherEnglishSpecializations.objects.filter(user=self.context.get('user')).first()
        if not user_english:
            return False
        elif instance in user_english.special.all():
            return True
        else:
            return False


class MathSpecializationsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MathSpecializations
        fields = ('name', 'status')

    def get_status(self, instance):
        user_math = TeacherMathSpecializations.objects.filter(user=self.context.get('user')).first()
        if not user_math:
            return False
        elif instance in user_math.special.all():
            return True
        else:
            return False


class AgeLearningSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = AgeLearning
        fields = ('name', 'status')

    def get_status(self, instance):
        user_age = TeacherAgeLearning.objects.filter(user=self.context.get('user')).first()
        if not user_age:
            return False
        elif instance in user_age.age_learning.all():
            return True
        else:
            return False


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


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')




class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalUserPurpose
        fields = ('user', 'subject')


class HelpSerializer(serializers.ModelSerializer):
    manager_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('manager_data',)

    def get_manager_data(self, instance):
        manager = ManagerToUser.objects.filter(user=instance).first().manager
        if not manager:
            return None
        serializer = DataManagerSerializer(manager)
        return serializer.data
