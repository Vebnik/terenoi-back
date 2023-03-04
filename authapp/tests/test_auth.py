import random

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from base.tests import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_auth_email(self):
        """ Авторизовать по почте """
        self.client = APIClient()
        response = self.client.post(
            reverse('authapp:login'),
            {'username': self.student.email, 'password': self.password}
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )

    def test_auth_email_case_insensitive(self):
        """ Авторизовать по почте в неправильном регистре """
        self.client = APIClient()
        response = self.client.post(
            reverse('authapp:login'),
            {'username': self.student.email.upper(), 'password': self.password}
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )

    def test_auth_phone(self):
        """ Авторизовать по номеру телефона """
        self.client = APIClient()
        response = self.client.post(
            reverse('authapp:login'),
            {'username': self.student.phone, 'password': self.password}
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )

    def test_auth_phone_with_mask(self):
        """ Авторизовать по номеру телефона со странной маской """
        self.client = APIClient()
        dirt_phone_number = self.make_dirt_phone(self.student.phone)
        response = self.client.post(
            reverse('authapp:login'),
            {'username': dirt_phone_number, 'password': self.password}
        )

        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
