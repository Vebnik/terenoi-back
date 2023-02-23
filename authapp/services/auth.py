import re
from django.conf import settings
from authapp.models import User


def find_username_by_phone_or_email(username):
    user_obj = User.objects.filter(email=username.lower(), is_verified=True).first()
    if user_obj:
        return user_obj.username
    else:
        username_for_phone = username.lower()
        for char in settings.PHONE_CHARACTERS:
            username_for_phone = username_for_phone.replace(char, '')

        user_obj = User.objects.filter(phone=username_for_phone, is_verified=True).first()
        if user_obj:
            return user_obj.username
    return None
