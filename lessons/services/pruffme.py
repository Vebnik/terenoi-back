import requests
import base64
import json
from django.conf import settings


class PruffMe:

    def __init__(self):
        self.url = 'https://pruffme.com/api/'
        self.user_key = settings.PRUFFME_API_USER
        self.password = settings.PRUFFME_API_SECRET

    def _send_request(self, action: str, content=None):
        if content is None:
            content = dict()
        json_string = json.dumps(content)
        base64_bytes = base64.b64encode(json_string.encode())

        body = {
            'user': self.user_key,
            'key': self.password,
            'action': action,
            'content': base64_bytes
        }

        result = requests.post(
            url=self.url,
            data=body
        )

        if result.status_code == 200:
            return result.json()

        print(result.status_code)
        print(result.text)
        return None

    def get_webinar_list(self):
        return self._send_request('webinars-list', {'limit': 10, 'offset': 0})

    def create_webinar(self, webinar):
        content = {
            'name': webinar.name,
            'use_record': 1,
            'time': {
                "selected_date": webinar.start_date.strftime('%Y-%m-%d %H:%M:%S'), #"2020-09-24 12:00:00",
                "duration": 60,
                "zone_offset": -360
            }
        }

        return self._send_request('webinar-create', content)

    def create_participant(self, webinar, user, role='participant'):

        content = {
            'webinar': webinar.hash,
            'user': {
                'email': user.email,
                'name': f'{user.first_name} {user.last_name}',
                'link': f'{settings.BACK_URL}/api/lessons/pruffme/done/?client={user.pk}&lesson={webinar.lesson.pk}',
                'role': role
            }
        }

        return self._send_request('create-participant', content)

    def get_webinar_record(self, webinar):
        content = {
            'webinar': webinar.hash,
            'limit': 10,
            'offset': 0
        }

        result = self._send_request('webinar-records', content)
        current_record = ''
        current_record_length = 0

        if 'result' in result and len(result.get('result')) > 0:
            result = result.get('result')[0]
            if result.get('children'):
                for child in result.get('children'):
                    if int(child.get('duration')) > current_record_length:
                        current_record = child.get('url')
                        current_record_length = int(child.get('duration'))
            else:
                if 'url' in result:
                    current_record = result.get('url')

        return current_record
