from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class WebHooksLeads(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print()
        body = f'{self.request.data}'
        subject = 'Сделки'
        send_mail(subject, body, settings.EMAIL_HOST_USER, ['sorulaijuli@gmail.com'], html_message=body)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksClients(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print()
        body = f'{self.request.data}'
        subject = 'Клиенты'
        send_mail(subject, body, settings.EMAIL_HOST_USER, ['sorulaijuli@gmail.com'], html_message=body)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksCustomers(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print()
        body = f'{self.request.data}'
        subject = 'Покупатели'
        send_mail(subject, body, settings.EMAIL_HOST_USER, ['sorulaijuli@gmail.com'], html_message=body)

        return Response({"message": "ok"}, status=status.HTTP_200_OK)