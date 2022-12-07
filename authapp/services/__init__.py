import datetime
import random
import time

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from sentry_sdk import capture_message, capture_exception

import AmoCRM
import authapp
import settings as set_app


def generate_password():
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


def slugify(string):
    letters = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "e",
        "ж": "j",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "y",
        "ы": "yi",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya"
    }
    for letter in string:
        if letter in letters:
            string = string.replace(letter, letters[letter])
    return string


def auth_alfa_account():
    data = {
        'email': settings.ALFA_EMAIL,
        'api_key': settings.ALFA_API_KEY
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/auth/login'
    response = requests.post(url=url, json=data)
    token = response.json().get('token')
    capture_message(token)
    return token


def _get_customer_index(token, page=0):
    headers = {
        'X-ALFACRM-TOKEN': token
    }
    data = {
        'study_status_id': 1,
        'page': page,
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/{1}/customer/index'

    response = requests.post(url=url, headers=headers, json=data)
    try:
        return response.json().get('items'), response.json().get('total')
    except:
        return [], 0


def _get_cgi_index(token, group_id):
    headers = {
        'X-ALFACRM-TOKEN': token
    }
    data = {
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/{1}/cgi/index?group_id={group_id}'

    response = requests.post(url=url, headers=headers, json=data)
    print(response.json())
    try:
        return response.json().get('items')
    except:
        return []


def get_cgi_alfa(token):
    for group in authapp.models.Group.objects.all():
        customers_alfa_ids = []
        for item in _get_cgi_index(token, group.alfa_id):
            customers_alfa_ids.append(item.get('customer_id', 0))

        list_of_users = list(authapp.models.User.objects.filter(alfa_id__in=customers_alfa_ids))
        group.students.add(*list_of_users)
        group.save()
        time.sleep(1)


def _get_group_index(token, page):
    headers = {
        'X-ALFACRM-TOKEN': token
    }
    data = {
        'page': page
    }
    url = f'{settings.ALFA_HOST_NAME}v2api/{1}/group/index'

    response = requests.post(url=url, headers=headers, json=data)
    print(response.json())
    try:
        return response.json().get('items'), response.json().get('total')
    except:
        return [], 0


def get_groups_alfa(token):
    page = 0
    limit_per_page = 20
    group_list, total_count = _get_group_index(token, page)
    while (page + 1) * limit_per_page <= total_count:
        groups_for_create = []
        for group in group_list:
            alfa_student = authapp.models.Group.objects.filter(alfa_id=group.get("id"))
            if not alfa_student:
                groups_for_create.append(
                    authapp.models.Group(
                        title=group.get('name'),
                        alfa_id=group.get("id"),
                        crm_data=group
                    )
                )

        authapp.models.Group.objects.bulk_create(
            groups_for_create,
            ignore_conflicts=True
        )

        time.sleep(1)
        page += 1
        group_list, total_count = _get_group_index(token, page)


def get_students_alfa(token):
    page = 0
    limit_per_page = 20
    student_list, total_count = _get_customer_index(token)
    while (page + 1) * limit_per_page <= total_count:
        users_for_create = []
        for student in student_list:
            alfa_student = authapp.models.User.objects.filter(alfa_id=student.get("id"))
            if not alfa_student:
                user_tmp_object = {
                    'password': '123qwe456rty',
                    'is_crm': True,
                    'crm_data': student
                }

                name_list = student.get('name').split(' ')[:2]

                user_tmp_object['username'] = slugify(f'{" ".join(name_list)}')
                user_tmp_object['alfa_id'] = student.get("id")

                if len(name_list) > 0:
                    user_tmp_object['first_name'] = name_list[0]
                if len(name_list) > 1:
                    user_tmp_object['last_name'] = name_list[1]

                user_tmp_object['birth_date'] = student.get('b_date').split(' ')[0]

                phones = student.get('phone')
                if phones:
                    student_phone = None
                    for index, phone in enumerate(phones):
                        if index == 0:
                            student_phone = phone
                            phones.remove(student_phone)
                    user_tmp_object['phone'] = student_phone

                users_for_create.append(
                    authapp.models.User(
                        **user_tmp_object
                    )
                )

        authapp.models.User.objects.bulk_create(
            users_for_create,
            ignore_conflicts=True
        )

        time.sleep(1)
        page += 1
        student_list, total_count = _get_customer_index(token, page)


def auth_amo_account():
    refresh_token = set_app.models.AmoCRMToken.objects.all()
    if not refresh_token:
        data = {
            "client_id": settings.AMO_ID,
            "client_secret": settings.AMO_SECRET_KEY,
            "grant_type": "authorization_code",
            "code": settings.AMO_TOKEN,
            "redirect_uri": settings.AMO_URL
        }
        res = requests.post(f'{settings.AMO_HOST_NAME}oauth2/access_token', json=data)
        if res.json().get('refresh_token'):
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
        res = requests.post(f'{settings.AMO_HOST_NAME}oauth2/access_token', json=data)
        set_app.models.AmoCRMToken.objects.create(refresh_token=res.json().get('refresh_token'))
        return res.json().get('access_token')


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
    capture_message(res.json())
    while True:
        try:
            leads = res.json().get('_embedded').get('leads')
            for i in leads:
                close_lead = i.get('closed_at')
                if not close_lead:
                    client = None
                    try:
                        id_contacst = i.get('_embedded').get('contacts')[0].get('id')
                        if id_contacst:
                            import time
                            time.sleep(1)
                            res_contacts = requests.get(f'{settings.AMO_HOST_NAME}api/v4/contacts/{id_contacst}',
                                                        headers=headers)
                            data_contacts = res_contacts.json()
                            client = AmoCRM.models.Clients.objects.filter(amo_id=int(data_contacts.get('id'))).first()
                            if not client:
                                custom_field = data_contacts.get('custom_fields_values')
                                if custom_field:
                                    for j in custom_field:
                                        if j.get('field_name') == 'Телефон':
                                            phone = j.get('values')[0].get('value')
                                            if phone:
                                                client = AmoCRM.models.Clients.objects.create(
                                                    amo_id=data_contacts.get('id'),
                                                    name=data_contacts.get('name'),
                                                    phone=phone)
                                else:
                                    client = AmoCRM.models.Clients.objects.create(amo_id=data_contacts.get('id'),
                                                                                  name=data_contacts.get('name')
                                                                                  )
                    except Exception as e:
                        capture_exception(e)
                        pass

                    lead = AmoCRM.models.Leads.objects.filter(amo_id=int(i.get('id')))
                    if not lead:
                        funnel_status = AmoCRM.models.FunnelStatus.objects.filter(
                            id_amo_funnel_status=int(i.get('status_id'))).first()
                        funnel = AmoCRM.models.Funnel.objects.filter(id_amo_funnel=int(i.get('pipeline_id'))).first()
                        ts = int(i.get('created_at'))
                        create = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                        ks = int(i.get('updated_at'))
                        update = datetime.datetime.utcfromtimestamp(ks).strftime('%Y-%m-%d %H:%M:%S')
                        AmoCRM.models.Leads.objects.create(amo_id=int(i.get('id')), name=i.get('name'),
                                                           price=int(i.get('price')),
                                                           funnel=funnel,
                                                           funnel_status=funnel_status, created_at=create,
                                                           updated_at=update,
                                                           client=client)
            next_page = res.json().get('_links').get('next').get('href')
            if next_page:
                res = requests.get(f'{next_page}', headers=headers, params=data)
            else:
                break
        except Exception:
            break


def add_func_customer(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        "mode": "periodicity",
        "is_enabled": True
    }
    res = requests.patch(f'{settings.AMO_HOST_NAME}api/v4/customers/mode', headers=headers, json=data)


def get_amo_customers(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'with': {
            'contacts': True
        }
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/customers', headers=headers, params=data)
    capture_message(res.json())
    while True:
        try:
            customers = res.json().get('_embedded').get('customers')
            for customer in customers:
                customer_custom_fields = customer.get('custom_fields_values')
                user = None
                client = None
                if customer_custom_fields:
                    for i in customer_custom_fields:
                        if i.get('field_name') == 'Имя ученика':
                            student_name_json = i.get('values')[0].get('value')
                            try:
                                student_first_name = student_name_json.split()[:2][1]
                                student_last_name = student_name_json.split()[:2][0]
                                user = authapp.models.User.objects.filter(first_name=student_first_name,
                                                                          last_name=student_last_name).first()
                            except Exception as e:
                                capture_exception(e)

                cust = AmoCRM.models.Customers.objects.filter(amo_id=customer.get('id'))
                if not cust:
                    next_date = datetime.datetime.utcfromtimestamp(int(customer.get('next_date'))).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    create = datetime.datetime.utcfromtimestamp(int(customer.get('created_at'))).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    update = datetime.datetime.utcfromtimestamp(int(customer.get('updated_at'))).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    status = AmoCRM.models.CustomerStatus.objects.filter(id_amo=customer.get('status_id')).first()
                    try:
                        client = AmoCRM.models.Clients.objects.filter(
                            amo_id=customer.get('_embedded').get('contacts')[0].get('id')).first()
                        if not client:
                            id = customer.get('_embedded').get('contacts')[0].get('id')
                            import time
                            time.sleep(1)
                            res_contacts = requests.get(f'{settings.AMO_HOST_NAME}api/v4/contacts/{id}',
                                                        headers=headers)
                            data_contacts = res_contacts.json()
                            custom_field = data_contacts.get('custom_fields_values')
                            phone = None
                            if custom_field:
                                for j in custom_field:
                                    if j.get('field_name') == 'Телефон':
                                        phone = j.get('values')[0].get('value')
                            client = AmoCRM.models.Clients.objects.create(
                                amo_id=data_contacts.get('id'),
                                name=data_contacts.get('name'),
                                phone=phone)

                    except Exception as e:
                        capture_exception(e)
                        pass

                    AmoCRM.models.Customers.objects.create(amo_id=customer.get('id'), name=customer.get('name'),
                                                           price=customer.get('next_price'), next_date=next_date,
                                                           status=status,
                                                           created_at=create, updated_at=update, client=client,
                                                           user=user)

            next_page = res.json().get('_links').get('next').get('href')
            if next_page:
                res = requests.get(f'{next_page}', headers=headers, params=data)
            else:
                break
        except Exception as e:
            capture_exception(e)
            break


def get_funnel(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/leads/pipelines', headers=headers)
    response = res.json().get('_embedded').get('pipelines')

    for item in response:
        funnel = AmoCRM.models.Funnel.objects.filter(id_amo_funnel=item.get('id'))
        if not funnel:
            funnel = AmoCRM.models.Funnel.objects.create(id_amo_funnel=item.get('id'), name=item.get('name'),
                                                         is_main=item.get('is_main'))
            for i in item.items():
                if i[0] == '_embedded':
                    statuses = i[1].get('statuses')
                    for status in statuses:
                        AmoCRM.models.FunnelStatus.objects.create(id_amo_funnel_status=status.get('id'),
                                                                  name=status.get('name'),
                                                                  funnel=funnel)


def get_customer_status(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/customers/statuses', headers=headers)
    response = res.json().get('_embedded').get('statuses')
    for item in response:
        status = AmoCRM.models.CustomerStatus.objects.filter(id_amo=item.get('id'))
        if not status:
            AmoCRM.models.CustomerStatus.objects.create(id_amo=item.get('id'), name=item.get('name'))
