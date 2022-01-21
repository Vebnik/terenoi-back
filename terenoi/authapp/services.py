import hashlib

import requests
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from voximplant.apiclient import VoximplantAPI, VoximplantException
import authapp.models


def send_verify_email(user):
    token = RefreshToken.for_user(user).access_token
    relative_link = 'api/auth/verify-email/'
    url = f'{settings.BASE_URL}/{relative_link}?token={token}'
    # context = {
    #     'static_url': settings.BACK_URL + settings.STATIC_URL,
    #     'front_url': settings.FRONT_URL,
    #     'url': url,
    #     'user': user,
    # }
    body = f'Для подтверждения учетной записи {user.username}  перейдите по ссылке: \n{url}'
    subject = 'Верификация почты'
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def create_voxi_account(username, display_name, password):
    api = VoximplantAPI("authapp/json/credentials.json")
    USER_NAME = username
    USER_DISPLAY_NAME = display_name
    USER_PASSWORD = password
    APPLICATION_ID = settings.VOXI_APPLICATION_ID
    try:
        res = api.add_user(USER_NAME,
                           USER_DISPLAY_NAME,
                           USER_PASSWORD,
                           application_id=APPLICATION_ID)
        user_voxi = authapp.models.VoxiAccount.objects.get(user__username=username)
        user_voxi.voxi_user_id = res.get('user_id')
        user_voxi.save()
    except VoximplantException as e:
        print("Error: {}".format(e.message))


def add_voxiaccount(user, username, display_name):
    password = f'{username}{username}'
    password_encode = hashlib.sha1(password.encode('utf-8')).hexdigest()[:9]
    authapp.models.VoxiAccount.objects.create(user=user, voxi_username=username, voxi_display_name=display_name,
                                              voxi_password=password_encode)
    create_voxi_account(username=username, display_name=display_name, password=password)
