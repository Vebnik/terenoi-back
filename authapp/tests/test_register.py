from authapp.models import User
from base.tests import BaseTestCase


class AuthTestCase(BaseTestCase):

    def test_create_user(self):
        """ Проверка адекватности создания и заполнения данных """
        phone_number = '333333333'
        dirt_phone_number = self.make_dirt_phone(phone_number)

        new_user = User.objects.create(
            username='test@test.com',
            email='test@test.com',
            phone=dirt_phone_number,
            password=self.password
        )

        self.assertEqual(
            new_user.phone,
            phone_number
        )
