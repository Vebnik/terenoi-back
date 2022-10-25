import pytz
from django.utils import timezone


class TimezoneMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            tz_str = request.user.time_zone
            timezone.activate(pytz.timezone(tz_str))
        else:
            timezone.deactivate()

        response = self.get_response(request)
        return response
