from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from authapp.models import User


class AccountTests(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        user_data = {
            'username': 'Julia',
            'email': 'email@me.com',
            'password': 'app12345',
            're_password': 'app12345'
        }
        return super(AccountTests, self).setUp()

    # def test_user_register_without_data(self):
    #     res = self.client.post(self.register_url)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self) -> None:
        return super(AccountTests, self).tearDown()
