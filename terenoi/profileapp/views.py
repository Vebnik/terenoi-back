from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authapp.models import User
from profileapp.models import TeacherSubject, Subject, ReferralPromo, UserParents, UserInterest, Interests, \
    LanguageInterface
from profileapp.permissions import IsStudent, IsTeacher
from profileapp.serializers import UpdateUserSerializer, UpdateStudentSerializer, UpdateTeacherSerializer, \
    ReferralSerializer
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
                        return super(ProfileUpdateView, self).update(request, *args, **kwargs)
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
                    return super(ProfileUpdateView, self).update(request, *args, **kwargs)
                else:
                    return Response({"message": "Такого города не существует."}, status=status.HTTP_404_NOT_FOUND)
            if request.data.get('parents_data'):
                for parent in request.data.get('parents_data'):
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
