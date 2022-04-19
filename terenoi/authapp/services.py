import hashlib
import random

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from voximplant.apiclient import VoximplantAPI, VoximplantException
import authapp
import settings as set_app
from authapp.decorators import create_voxi_file
import profileapp


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


def auth_alfa_account():
    data = {
        'email': settings.ALFA_EMAIL,
        'api_key': settings.ALFA_API_KEY
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/auth/login'
    response = requests.post(url=url, json=data)
    token = response.json().get('token')
    return token


def get_students_alfa(token):
    headers = {
        'X-ALFACRM-TOKEN': token
    }
    data = {
        'study_status_id': 1
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/{1}/customer/index'
    response = requests.post(url=url, headers=headers, json=data)
    student_list = response.json().get('items')
    for student in student_list:
        alfa_student = authapp.models.User.objects.filter(alfa_id=student.get("id"))
        if alfa_student:
            pass
        else:
            username = f'student_alfa_{student.get("id")}'
            name = student.get('name').split(' ')[:2]
            alfa_id = student.get("id")
            first_name = name[1]
            last_name = name[0]
            student_phone = None
            phones = student.get('phone')
            b_date = student.get('b_date').split(' ')[0]
            if phones:
                for index, phone in enumerate(phones):
                    if index == 0:
                        student_phone = phone
                        phones.remove(student_phone)
                user = authapp.models.User.objects.create_user(username=username, first_name=first_name,
                                                               last_name=last_name,
                                                               phone=student_phone, password='qwe123rty456',
                                                               birth_date=b_date,
                                                               is_crm=True, alfa_id=alfa_id)
            else:
                user = authapp.models.User.objects.create_user(username=username, first_name=first_name,
                                                               last_name=last_name,
                                                               password='qwe123rty456',
                                                               birth_date=b_date,
                                                               is_crm=True, alfa_id=alfa_id)
            if phones:
                for phone in phones:
                    profileapp.models.UserParents.objects.create(user=user, parent_phone=phone)


def auth_amo_account():
    refresh_token = set_app.models.AmoCRMToken.objects.all()
    amo_token = str(settings.AMO_TOKEN)
    if not refresh_token:
        data = {
            "client_id": settings.AMO_ID,
            "client_secret": settings.AMO_SECRET_KEY,
            "grant_type": "authorization_code",
            "code": amo_token,
            "redirect_uri": settings.AMO_URL
        }
        res = requests.post(f'{settings.AMO_HOST_NAME}oauth2/access_token', data=data)
        set_app.models.AmoCRMToken.objects.create(refresh_token=res.json().get('refresh_token'))
        return res.json().get('access_token')
    else:
        ref_token = set_app.models.AmoCRMToken.objects.all().first().refresh_token
        data = {
            "client_id": settings.AMO_ID,
            "client_secret": settings.AMO_SECRET_KEY,
            "grant_type": "refresh_token",
            "refresh_token": ref_token,
            "redirect_uri": settings.AMO_URL
        }
        res = requests.post(f'{settings.AMO_HOST_NAME}oauth2/access_token', data=data)
        set_app.models.AmoCRMToken.objects.create(refresh_token=res.json().get('refresh_token'))
        return res.json().get('access_token')

        # headers = {
        #     'Authorization': f'Bearer {token}'
        # }
        # res_1 = requests.get('https://sorulai.amocrm.ru/api/v4/leads', headers=headers)
        # print(res_1.json())


def get_amo_leads(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'with': {
            'contacts': True
        }
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/leads', headers=headers, params=data)
    print('leads')
    print(res.json())


def add_func_customer(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        "mode": "segments",
        "is_enabled": True
    }
    res = requests.patch(f'{settings.AMO_HOST_NAME}api/v4/customers/mode', headers=headers, json=data)


def get_amo_customers(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/customers', headers=headers)
    print('customers')
    print(res.json())
