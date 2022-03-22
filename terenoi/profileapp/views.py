from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.models import User, UserStudyLanguage, StudyLanguage
from profileapp.models import TeacherSubject, Subject, ReferralPromo, UserParents, UserInterest, Interests, \
    LanguageInterface, ManagerToUser, ManagerRequestsPassword, TeacherAgeLearning, AgeLearning, \
    TeacherMathSpecializations, MathSpecializations, EnglishSpecializations, TeacherEnglishSpecializations, \
    EnglishLevel, TeacherEnglishLevel
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer, \
    ReferralSerializer, UserParentsSerializer, ChangePasswordSerializer
from settings.models import CityTimeZone, UserCity


class ProfileUpdateView(generics.UpdateAPIView):
    """Редактирование пользователя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get_serializer_class(self):
        user = self.get_object()
        if user.is_teacher or user.is_superuser:
            return UpdateTeacherSerializer
        else:
            return UpdateStudentSerializer

    def update(self, request, *args, **kwargs):
        try:
            if request.data.get('subject'):
                for sub in request.data.get('subject'):
                    subject = Subject.objects.filter(name=sub).first()
                    if subject:
                        TeacherSubject.objects.create(user=self.request.user, subject=subject)
                        # return super(ProfileUpdateView, self).update(request, *args, **kwargs)
                else:
                    return Response({"message": "Такого предмета не существует."}, status=status.HTTP_404_NOT_FOUND)
            if request.data.get('city'):
                city = CityTimeZone.objects.filter(city=request.data.get('city').get('city_title')).first()
                if city:
                    user_city = UserCity.objects.filter(user=self.request.user).first()
                    if user_city:
                        user_city.city = city
                        user_city.save()
                    else:
                        UserCity.objects.create(user=self.request.user, city=city)
                else:
                    return Response({"message": "Такого города не существует."}, status=status.HTTP_404_NOT_FOUND)
            if request.data.get('parents_data'):
                for parent in request.data.get('parents_data'):
                    if parent.get('pk'):
                        parent_user = UserParents.objects.filter(pk=int(parent.get('pk'))).first()
                        if parent_user:
                            UserParents.objects.filter(pk=int(parent.get('pk'))).update(
                                full_name=parent.get('full_name'),
                                parent_phone=parent.get('parent_phone'), parent_email=parent.get('parent_email'))
                        else:
                            UserParents.objects.create(user=self.request.user, full_name=parent.get('full_name'),
                                                       parent_phone=parent.get('parent_phone'),
                                                       parent_email=parent.get('parent_email'))

                    else:
                        UserParents.objects.create(user=self.request.user, full_name=parent.get('full_name'),
                                                   parent_phone=parent.get('parent_phone'),
                                                   parent_email=parent.get('parent_email'))
            if request.data.get('interests'):
                for interest in request.data.get('interests'):
                    user_interest = UserInterest.objects.filter(user=self.request.user).first()
                    interest_l = Interests.objects.filter(name=interest.get('name')).first()
                    if interest.get('status'):
                        if user_interest:
                            user_interest.interests.add(interest_l)
                            user_interest.save()
                        else:
                            instance = UserInterest.objects.create(user=self.request.user)
                            instance.interests.set(interest_l)
                    else:
                        if user_interest:
                            user_interest.interests.remove(interest_l)
                            user_interest.save()
            if request.data.get('language_interface'):
                lang_interface = LanguageInterface.objects.filter(user=self.request.user).first()
                if lang_interface:
                    if request.data.get('language_interface').get('interface_language') == LanguageInterface.RUSSIAN:
                        lang_interface.interface_language = LanguageInterface.RUSSIAN
                    elif request.data.get('language_interface').get('interface_language') == LanguageInterface.KAZAKH:
                        lang_interface.interface_language = LanguageInterface.KAZAKH
                    else:
                        lang_interface.interface_language = LanguageInterface.ENGLISH
                    lang_interface.save()
                else:
                    if request.data.get('language_interface').get('interface_language') == LanguageInterface.RUSSIAN:
                        LanguageInterface.objects.create(user=self.request.user,
                                                         interface_language=LanguageInterface.RUSSIAN)
                    elif request.data.get('language_interface').get('interface_language') == LanguageInterface.KAZAKH:
                        LanguageInterface.objects.create(user=self.request.user,
                                                         interface_language=LanguageInterface.KAZAKH)
                    else:
                        LanguageInterface.objects.create(user=self.request.user,
                                                         interface_language=LanguageInterface.ENGLISH)
            if request.data.get('language'):
                user_language = UserStudyLanguage.objects.filter(user=self.request.user).first()
                if not user_language:
                    user_study = UserStudyLanguage.objects.create(user=self.request.user)
                    for lang in request.data.get('language'):
                        language = StudyLanguage.objects.filter(name=lang.get('name')).first()
                        user_study.language.add(language)
                    user_study.save()
                else:
                    user_language.delete()
                    user_study = UserStudyLanguage.objects.create(user=self.request.user)
                    for lang in request.data.get('language'):
                        language = StudyLanguage.objects.filter(name=lang.get('name')).first()
                        user_study.language.add(language)
                    user_study.save()

            if request.data.get('age'):
                for age in request.data.get('age'):
                    user_age = TeacherAgeLearning.objects.filter(user=self.request.user).first()
                    age_l = AgeLearning.objects.filter(name=age.get('name')).first()
                    if age.get('status'):
                        if user_age:
                            user_age.age_learning.add(age_l)
                            user_age.save()
                        else:
                            instance = TeacherAgeLearning.objects.create(user=self.request.user)
                            instance.age_learning.set(age_l)
                    else:
                        if user_age:
                            user_age.age_learning.remove(age_l)
                            user_age.save()
            if request.data.get('math_special'):
                for math in request.data.get('math_special'):
                    user_math = TeacherMathSpecializations.objects.filter(user=self.request.user).first()
                    math_l = MathSpecializations.objects.filter(name=math.get('name')).first()
                    if math.get('status'):
                        if user_math:
                            user_math.special.add(math_l)
                            user_math.save()
                        else:
                            instance = TeacherMathSpecializations.objects.create(user=self.request.user)
                            instance.special.set(math_l)
                    else:
                        if user_math:
                            user_math.special.remove(math_l)
                            user_math.save()
            if request.data.get('english_special'):
                for eng in request.data.get('english_special'):
                    user_eng = TeacherEnglishSpecializations.objects.filter(user=self.request.user).first()
                    eng_l = EnglishSpecializations.objects.filter(name=eng.get('name')).first()
                    if eng.get('status'):
                        if user_eng:
                            user_eng.special.add(eng_l)
                            user_eng.save()
                        else:
                            instance = TeacherMathSpecializations.objects.create(user=self.request.user)
                            instance.special.set(eng_l)
                    else:
                        if user_eng:
                            user_eng.special.remove(eng_l)
                            user_eng.save()
            if request.data.get('level'):
                for lvl in request.data.get('level'):
                    user_lvl = TeacherEnglishLevel.objects.filter(user=self.request.user).first()
                    lvl_l = EnglishLevel.objects.filter(name=lvl.get('name')).first()
                    if lvl.get('status'):
                        if user_lvl:
                            user_lvl.level.add(lvl_l)
                            user_lvl.save()
                        else:
                            instance = TeacherEnglishLevel.objects.create(user=self.request.user)
                            instance.level.set(lvl_l)
                    else:
                        if user_lvl:
                            user_lvl.level.remove(lvl_l)
                            user_lvl.save()
            if request.data.get('language'):
                for lang in request.data.get('language'):
                    user_lang = UserStudyLanguage.objects.filter(user=self.request.user).first()
                    l_lang = StudyLanguage.objects.filter(name=lang.get('name')).first()
                    if lang.get('status'):
                        if user_lang:
                            user_lang.language.add(l_lang)
                            user_lang.save()
                        else:
                            instance = UserStudyLanguage.objects.create(user=self.request.user)
                            instance.language.set(l_lang)
                    else:
                        if user_lang:
                            user_lang.language.remove(l_lang)
                            user_lang.save()


        except AttributeError:
            return super(ProfileUpdateView, self).update(request, *args, **kwargs)
        return super(ProfileUpdateView, self).update(request, *args, **kwargs)


class ProfileView(APIView):
    """Просмотр профиля пользователя"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        if user.is_teacher or user.is_superuser:
            serializer = UpdateTeacherSerializer(user)
            return Response(serializer.data)
        else:
            serializer = UpdateStudentSerializer(user)
            return Response(serializer.data)


class ReferralView(APIView):
    """Получение реферального кода"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self, request):
        user = self.get_object()
        promo = ReferralPromo.objects.filter(user=user).first()
        serializer = ReferralSerializer(promo)
        return Response(serializer.data)


class DeleteParentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserParents.objects.all()
    serializer_class = UserParentsSerializer


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def update(self, request, *args, **kwargs):
        manager = ManagerToUser.objects.get(user=self.request.user).manager
        if self.request.data.get('password'):
            ManagerRequestsPassword.objects.create(manager=manager, user=self.request.user,
                                                   new_password=self.request.data.get('password'))
            return Response({'message': 'Запрос на изменение пароля отправлен'},
                            status=status.HTTP_200_OK)
        return super(ChangePasswordView, self).update(request, *args, **kwargs)
