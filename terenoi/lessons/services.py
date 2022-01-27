import pytz
from django.conf import settings


def current_date(user, date):
    user_timezone = pytz.timezone(user.time_zone or settings.TIME_ZONE)
    return date.astimezone(user_timezone)

