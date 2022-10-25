import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from authapp.models import User


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope.get('user')
        self.room_name = f'{user.username}'
        self.room_group_name = f'{user.username}_group'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()
        self.update_user_status(user, True)
        self.send(text_data=json.dumps({'status': 'connected from django channels'}))

    def receive(self, text_data):
        self.send(text_data=json.dumps({'status': 'we got you'}))

    def disconnect(self, code):
        user = self.scope["user"]
        self.update_user_status(user, False)

    def send_notification(self, event):
        self.user = self.scope["user"]
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload': data}))

    def update_user_status(self, user, status):
        User.objects.filter(pk=user.pk).update(is_online=status)

