import pytz
from django.utils import timezone
from django.conf import settings


class TimezoneMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            tz_str = settings.TIME_ZONE_MANAGER
            timezone.activate(pytz.timezone(tz_str))
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
