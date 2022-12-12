import http
import json
from typing import Any

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from authapp.models import User


class BaseTestCase(APITestCase):
    """
        Базовый класс для тестирования всего проекта
    """
    access_token: str
    student_username = 'student'
    teacher_username = 'teacher'
    password = '123qwe456rty'
    student = None
    teacher = None

    def setUp(self) -> None:
        self.student = User.objects.create_user(
            username=self.student_username,
            password=self.password,
            first_name='Student',
            last_name='Student',
            is_student=True,
            is_teacher=False
        )
        self.teacher = User.objects.create_user(
            username=self.teacher_username,
            password=self.password,
            first_name='Teacher',
            last_name='Teacher',
            is_student=False,
            is_teacher=True
        )
        self.student_client = APIClient()
        response = self.student_client.post(
            reverse('authapp:login'),
            {'username': self.student_username, 'password': self.password}
        )
        self.student_access_token = response.json().get('access')

        self.teacher_client = APIClient()
        response = self.teacher_client.post(
            reverse('authapp:login'),
            {'username': self.teacher_username, 'password': self.password}
        )
        self.teacher_access_token = response.json().get('access')

    def _make_request(self, method: str, url: str, client: str = 'student', data: dict = None, status_code: int = http.HTTPStatus.OK,
                      headers: dict = None) -> dict:
        if client == 'student':
            headers_to_send = {"HTTP_AUTHORIZATION": f'Bearer {self.student_access_token}'}
        else:
            headers_to_send = {"HTTP_AUTHORIZATION": f'Bearer {self.teacher_access_token}'}
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
        return self._make_request('POST', url, data, status_code=status_code, headers=headers)

    def _make_get(self, url: str, params: dict = None, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('GET', url, params, status_code, headers)

    def _make_patch(self, url: str, data: dict, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('PATCH', url, data, status_code, headers)

    def _make_put(self, url: str, data: dict, status_code: int = http.HTTPStatus.OK, headers: dict = None):
        return self._make_request('PUT', url, data, status_code, headers)

    def _make_delete(self, url: str, data: dict = None, status_code: int = http.HTTPStatus.NO_CONTENT,
                     headers: dict = None):
        return self._make_request('DELETE', url, data, status_code, headers)
