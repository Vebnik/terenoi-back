from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken


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
