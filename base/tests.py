import http
import json
import random
from typing import Any

import pytz
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from authapp.models import User


class BaseTestCase(APITestCase):
    """
        Базовый класс для тестирования всего проекта
    """
    access_token: str
    student = None
    teacher = None
    password = '123qwe456rty'

    def setUp(self) -> None:
        self.maxDiff = None
        self.student = User.objects.create_user(
            username='student@student.com',
            email='student@student.com',
            password=self.password,
            first_name='Student',
            last_name='Student',
            phone='111111111',
            is_verified=True,
            is_student=True,
            is_teacher=False,
        )
        self.user_worker = User.objects.create_user(
            username='teacher@teacher.com',
            email='teacher@teacher.com',
            password=self.password,
            first_name='Teacher',
            last_name='Teacher',
            phone='222222222',
            is_verified = True,
            is_teacher=True,
            is_student=False,
        )

    @staticmethod
    def _get_serialized_data(user, serializer_class):
        """ Метод для возврата сериализованных данных """
        return serializer_class(user).data

    @staticmethod
    def _get_datetime_with_tz_as_string(datetime_item):
        return datetime_item. \
            astimezone(pytz.timezone(settings.TIME_ZONE)). \
            strftime(settings.DATETIME_FORMAT)

    @staticmethod
    def make_dirt_phone(phone_number):
        phone_with_mask = ''
        for i in phone_number:
            phone_with_mask += i + random.sample(settings.PHONE_CHARACTERS, 1)[0]
        return phone_with_mask

    def _login(self, username):
        self.client = APIClient()
        response = self.client.post(
            reverse('users:login'),
            {'username': username, 'password': self.password}
        )
        self.access_token = response.json().get('access')

    def _make_request(self, method: str, url: str, username: str, data: dict = None, status_code: int = http.HTTPStatus.OK,
                      headers: dict = None) -> dict:
        """ Метод для формирования запроса с авторизацией и TODO: тестированием закрытого доступа """
        self._login(username)
        headers_to_send = {"HTTP_AUTHORIZATION": f'Bearer {self.access_token}'}
        if headers is not None:
            headers_to_send.update(headers)
        request_data = {
            'path': url,
            'content_type': 'application/json',
        }

        request_data.update(headers_to_send)
        if data and method.lower() != 'get':
            request_data['data'] = json.dumps(data)
        elif method.lower() == 'get':
            request_data['data'] = data

        response = None

        if method == 'POST':
            response = self.client.post(
                **request_data
            )
        elif method == 'GET':
            response = self.client.get(
                **request_data
            )
            print(request_data['data'])
        elif method == 'PATCH':
            response = self.client.patch(
                **request_data
            )
        elif method == 'PUT':
            response = self.client.put(
                **request_data
            )
        elif method == 'DELETE':
            response = self.client.delete(
                **request_data
            )

        self.assertIsNotNone(response)
        if method != 'DELETE':
            print(response.json())

        self.assertEqual(response.status_code, status_code)
        if method != 'DELETE':
            return response.json()

    def _make_post(self, url: str, data: Any, status_code: int, headers: dict = None):
        return self._make_request('POST', url, data, status_code, headers)

    def _make_get(self, url: str, params: dict = None, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('GET', url, params, status_code, headers)

    def _make_patch(self, url: str, data: dict, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('PATCH', url, data, status_code, headers)

    def _make_put(self, url: str, data: dict, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('PUT', url, data, status_code, headers)

    def _make_delete(self, url: str, data: dict = None, status_code: int = http.HTTPStatus.NO_CONTENT,
                     headers: dict = None):
        return self._make_request('DELETE', url, data, status_code, headers)
