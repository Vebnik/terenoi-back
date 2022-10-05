import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from sentry_sdk import capture_message

import authapp
from AmoCRM.models import Leads, Funnel, FunnelStatus, Clients, Customers, CustomerStatus
from AmoCRM.services import get_amo_contact_leads, get_leads_data, get_contacts_data, get_customer_user, \
    get_leads_data_add, get_customer_data
from authapp.services import auth_amo_account


class WebHooksLeads(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        capture_message(self.request.data)
        if self.request.data:
            res = self.request.data
            amo_token = auth_amo_account()
            if res.get('leads[update][0][id]'):
                lead_id = res.get('leads[update][0][id]')
                lead = Leads.objects.filter(amo_id=lead_id).first()
                if lead:
                    data = get_leads_data_add(res, amo_token, lead_id)
                    lead.name = res.get('leads[update][0][name]')
                    lead.price = res.get('leads[update][0][price]')
                    lead.funnel = data[0]
                    lead.funnel_status = data[1]
                    if data[2]:
                        lead.client = data[2]
                    lead.save()
            elif res.get('leads[add][0][id]'):
                lead = Leads.objects.filter(amo_id=res.get('leads[add][0][id]')).first()
                if not lead:
                    lead_id = res.get('leads[add][0][id]')
                    data = get_leads_data_add(res, amo_token, lead_id)
                    if data[2]:
                        Leads.objects.create(amo_id=res.get('leads[add][0][id]'), name=res.get('leads[add][0][name]'),
                                             price=res.get('leads[add][0][price]'),
                                             funnel=data[0],
                                             funnel_status=data[1],
                                             client=data[2])
                    else:
                        Leads.objects.create(amo_id=res.get('leads[add][0][id]'), name=res.get('leads[add][0][name]'),
                                             price=res.get('leads[add][0][price]'),
                                             funnel=data[0],
                                             funnel_status=data[1])
            else:
                if res.get('leads[delete][0][id]'):
                    try:
                        Leads.objects.filter(amo_id=res.get('leads[delete][0][id]')).first().delete()
                    except Exception:
                        pass
            return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksClients(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        capture_message(self.request.data)
        if self.request.data:
            res = self.request.data
            amo_token = auth_amo_account()
            if res.get('contacts[update][0][id]'):
                contact = Clients.objects.filter(amo_id=res.get('contacts[update][0][id]')).first()
                if contact:
                    contact.name = res.get('contacts[update][0][name]')
                    phone = get_contacts_data(i=res, token=amo_token)
                    if phone:
                        contact.phone = phone
                    contact.save()
            elif res.get('contacts[add][0][id]'):
                contact = Clients.objects.filter(amo_id=res.get('contacts[add][0][id]')).first()
                if not contact:
                    phone = get_contacts_data(i=res, token=amo_token)
                    Clients.objects.create(amo_id=res.get('contacts[add][0][id]'),
                                           name=res.get('contacts[add][0][name]'), phone=phone)
            else:
                if res.get('contacts[delete][0][id]'):
                    try:
                        Clients.objects.filter(amo_id=res.get('contacts[delete][0][id]')).first().delete()
                    except Exception:
                        pass
            return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksCustomers(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        capture_message(self.request.data)
        if self.request.data:
            res = self.request.data
            amo_token = auth_amo_account()
            if res.get('customers[update][0][id]'):
                customer_id = res.get('customers[update][0][id]')
                customer = Customers.objects.filter(amo_id=customer_id).first()
                if customer:
                    user = get_customer_user(customer_id, amo_token)
                    data = get_customer_data(amo_token, customer_id)
                    customer.name = res.get('customers[update][0][name]')
                    if res.get('customers[update][0][next_price]'):
                        customer.price = res.get('customers[update][0][next_price]')
                    if data[0]:
                        customer.status = data[0]
                    customer.next_date = data[4]
                    customer.created_at = data[1] if data[1] else None
                    customer.updated_at = data[2] if data[2] else None
                    if user:
                        customer.user = user
                    if data[3]:
                        customer.client = data[3]
                    customer.save()
            elif res.get('customers[add][0][id]'):
                customer = Customers.objects.filter(amo_id=res.get('customers[add][0][id]')).first()
                if not customer:
                    customer_id = res.get('customers[add][0][id]')
                    data = get_customer_data(amo_token, customer_id)
                    user = get_customer_user(customer_id, amo_token)
                    cus = Customers.objects.create(amo_id=res.get('customers[add][0][id]'),
                                                   name=res.get('customers[add][0][name]'),
                                                   price=res.get('customers[add][0][next_price]'),
                                                   next_date=data[4], created_at=data[1], updated_at=data[2],
                                                   status=data[0])
                    if data[3]:
                        cus.client = data[3]
                    if user:
                        cus.user = user
                    cus.save()
            else:
                if res.get('customers[delete][0][id]'):
                    try:
                        Customers.objects.filter(amo_id=res.get('customers[delete][0][id]')).first().delete()
                    except Exception:
                        pass
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
