import re
from authapp.models import User


def find_username_by_phone_or_email(username):

    reg_exp_pattern = re.compile(r"\+|\(|\)| |-")
    user_by_email = User.objects.filter(email=username.lower()).first()
    user_by_phone = User.objects.filter(phone=re.sub(reg_exp_pattern, '', username.lower())).first()

    if user_by_email and (user_by_email.is_staff or user_by_email.is_superuser or user_by_email.is_verified):
        return user_by_email.username

    if user_by_phone and (user_by_phone.is_staff or user_by_phone.is_superuser or user_by_phone.is_verified):
        return user_by_phone.username
