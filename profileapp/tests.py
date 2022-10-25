import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from rest_framework_simplejwt.tokens import RefreshToken

from authapp.models import User


class ProfileTests(APITestCase):
    def setUp(self) -> None:
        self.student = User.objects.create_user(username='Julia', password='app123456', email='student@yandex.ru',
                                                is_student=True, first_name="Julia",
                                                is_verified=True)
        self.teacher = User.objects.create_user(username='Mark', password='app123456', email='teacher@yandex.ru',
                                                is_teacher=True,
                                                is_verified=True)

        self.manager = User.objects.create_user(username='Galya', password='app123456', email='manager@yandex.ru',
                                                is_staff=True,
                                                is_verified=True)

        return super(ProfileTests, self).setUp()

    def test_profile(self):
        token_student = RefreshToken.for_user(self.student).access_token
        token_teacher = RefreshToken.for_user(self.teacher).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_student}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_teacher}')
        res_student = self.client.get(path=reverse('profile:profile'))
        res_teacher = self.client.get(path=reverse('profile:profile'))
        self.assertEqual(res_student.status_code, status.HTTP_200_OK)
        self.assertEqual(res_teacher.status_code, status.HTTP_200_OK)

    def test_update_valid_data_student(self):
        token_student = RefreshToken.for_user(self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_student}')
        data = {
            "username": self.student.username,
            "first_name": "Maria",
            "last_name": "Ivanova",
            "gender": "F",
            "birth_date": "1998-08-08",
            "city": {
                "city_title": "Алма-Ата"
            },
            "parents_data": [],
            "purposes": [],
            "interests": [
                {
                    "name": "Спорт",
                    "status": True
                },
                {
                    "name": "Путешествия",
                    "status": False
                },
                {
                    "name": "Языки",
                    "status": True
                },
                {
                    "name": "Наука",
                    "status": False
                },
                {
                    "name": "Музыка",
                    "status": False
                },
                {
                    "name": "Экономика",
                    "status": False
                }
            ],
            "language": [
                {
                    "name": "Английский",
                    "status": False
                },
                {
                    "name": "Русский",
                    "status": True
                },
                {
                    "name": "Казахский",
                    "status": False
                }
            ],
            "time_zone": "Asia/Almaty",
            "phone": "897957575",
            "bio": "Hello",
            "language_interface": {
                "interface_language": "RU"
            }
        }
        res_student = self.client.put(path=reverse('profile:update_profile'), data=json.dumps(data),
                                      content_type='application/json')
        self.assertEqual(res_student.status_code, status.HTTP_200_OK)

    def test_update_without_username_student(self):
        token_student = RefreshToken.for_user(self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_student}')
        data = {
            'first_name': 'Maria',
            'last_name': 'Petrova'
        }
        res_student = self.client.put(path=reverse('profile:update_profile'), data=json.dumps(data),
                                      content_type='application/json')
        self.assertEqual(res_student.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self) -> None:
        return super(ProfileTests, self).tearDown()
