import hashlib
import random

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from voximplant.apiclient import VoximplantAPI, VoximplantException
import authapp.models
from authapp.decorators import create_voxi_file


def generatePassword():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 8
    promo = ''
    while True:
        for i in range(length):
            promo += random.choice(chars)
        break
    return promo


def send_verify_email(user):
    token = RefreshToken.for_user(user).access_token
    relative_link = 'verify-email/'
    small_url = f'{settings.BASE_URL}/{relative_link}'
    url = f'{settings.BASE_URL}/{relative_link}?token={token}'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'url': url,
        'user': user,
        'email': settings.EMAIL_HOST_USER,
        'small_url': small_url
    }
    body = render_to_string('emails/mail-verify-email.html', context)
    subject = 'Верификация почты'
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_generate_data(user, password):
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'password': password
    }
    body = render_to_string('emails/generate_new_data.html', context)
    subject = 'Данные для входа'
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_notifications(user, subject, text, lesson_date=None):
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
        'lesson_date': lesson_date
    }
    body = render_to_string('emails/notification_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_transfer_lesson(user, lesson):
    text = f'Пользователь {user.first_name} {user.last_name} хочет перенести урок {lesson.pk}'
    subject = 'Перенос урока'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_cancel_lesson(user, lesson):
    text = f'Пользователь {user.first_name} {user.last_name} хочет отменить урок {lesson.pk}'
    subject = 'Отмена урока'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_accept_transfer_lesson(user, lesson):
    text = f'Пользователь {user.first_name} {user.last_name} подтвердил перенос урока {lesson.pk}'
    subject = 'Подтверждение переноса'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_accept_cancel_lesson(user, lesson):
    text = f'Пользователь {user.first_name} {user.last_name} подтвердил отмену урока {lesson.pk}'
    subject = 'Подтверждение отмены'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_reject_transfer_lesson(user, lesson):
    text = f'Пользователь {user.username}  отклонил перенос урока {lesson.pk}'
    subject = 'Отклонение переноса'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


def send_reject_cancel_lesson(user, lesson):
    text = f'Пользователь {user.username}  отклонил отмену урока {lesson.pk}'
    subject = 'Отклонение отмены'
    context = {
        'static_url': settings.BACK_URL + settings.STATIC_URL,
        'front_url': settings.FRONT_URL,
        'user': user,
        'body': text,
        'title': subject,
    }
    body = render_to_string('emails/transfer_email.html', context)
    send_mail(subject, body, settings.EMAIL_HOST_USER, [user.email], html_message=body)


@create_voxi_file
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

        user_voxi = authapp.models.VoxiAccount.objects.get(voxi_username=username)
        user_voxi.voxi_user_id = res.get('user_id')
        user_voxi.save()
    except VoximplantException as e:
        print("Error: {}".format(e.message))


def add_voxiaccount(user, username, display_name):
    password = f'{user.username}{user.username}'
    # password_encode = hashlib.sha1(password.encode('utf-8')).hexdigest()[:9]
    authapp.models.VoxiAccount.objects.create(user=user, voxi_username=username, voxi_display_name=display_name,
                                              voxi_password=password)
    create_voxi_account(username=username, display_name=display_name, password=password)
