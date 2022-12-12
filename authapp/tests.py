import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authapp.models import User


class AccountTests(APITestCase):
    def setUp(self) -> None:
        self.user_valid_data = {
            'username': 'Julia',
            'email': 'email@me.com',
            'password': 'app12345',
            're_password': 'app12345'
        }
        self.user_invalid_data_email = {
            'username': 'Julia',
            'email': 'email@me',
            'password': 'app12345',
            're_password': 'app12345'
        }

        self.user_invalid_data_email = {
            'username': 'Julia',
            'email': 'email@me.com',
            'password': 'app12345',
            're_password': 'app123458'
        }
        self.user2_invalid_data_email = {
            'username': 'Mark',
            'email': 'email@me.com',
            'password': 'app12345',
            're_password': 'app12345'
        }
        self.user2_invalid_data_username = {
            'username': 'Julia',
            'email': 'emailtwo@me.com',
            'password': 'app12345',
            're_password': 'app12345'
        }
        return super(AccountTests, self).setUp()

    def test_user_register_without_data(self):
        res = self.client.post(path=reverse('authapp:register'))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_correct(self):
        res = self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_valid_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_register_incorrect_email(self):
        res = self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_invalid_data_email),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_incorrect_password(self):
        res = self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_invalid_data_email),
                               content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_register_similar_email_and_username(self):
        self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_valid_data),
                         content_type='application/json')
        res_2 = self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user2_invalid_data_email),
                                 content_type='application/json')
        res_3 = self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user2_invalid_data_username),
                                 content_type='application/json')
        self.assertEqual(res_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_link(self):
        self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_valid_data),
                         content_type='application/json')
        user = User.objects.get(username=self.user_valid_data.get('username'))
        token = RefreshToken.for_user(user).access_token
        verify_url = f'http://127.0.0.1:8080/api/auth/verify-email/?token={token}'
        res = self.client.get(path=verify_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        self.client.post(path=reverse('authapp:register'), data=json.dumps(self.user_valid_data),
                         content_type='application/json')
        user = User.objects.get(username=self.user_valid_data.get('username'))
        user.is_verified = True
        user.save()
        res = self.client.post(path=reverse('authapp:login'),
                               data=json.dumps({'username': self.user_valid_data['email'],
                                                'password': self.user_valid_data['password']}),
                               content_type='application/json')
        res_2 = self.client.post(path=reverse('authapp:login'),
                                 data=json.dumps({'username': 'Juli',
                                                  'password': self.user_valid_data['password']}),
                                 content_type='application/json')
        res_3 = self.client.post(path=reverse('authapp:login'),
                                 data=json.dumps({'username': self.user_valid_data['email'],
                                                  'password': 'app12345678'}),
                                 content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_3.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self) -> None:
        return super(AccountTests, self).tearDown()
