import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

import authapp
from AmoCRM.models import Leads, Funnel, FunnelStatus, Clients, Customers, CustomerStatus
from AmoCRM.services import get_amo_contact_leads, get_leads_data, get_contacts_data, get_customer_user, \
    get_customer_data
from authapp.services import auth_amo_account


class WebHooksLeads(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if self.request.data:
            res = self.request.data
            amo_token = auth_amo_account()
            if res.get('leads').get('update'):
                for i in res.get('leads').get('update'):
                    lead_id = i.get('id')
                    lead = Leads.objects.filter(amo_id=lead_id).first()
                    if lead:
                        data = get_leads_data(i, amo_token, lead_id)
                        lead.name = i.get('name')
                        lead.price = i.get('price')
                        lead.funnel = data[0]
                        lead.funnel_status = data[1]
                        lead.created_at = data[2] if data[2] else None
                        lead.updated_at = data[3] if data[3] else None
                        if data[4]:
                            lead.client = data[4]
                        lead.save()
            elif res.get('leads').get('add'):
                for i in res.get('leads').get('add'):
                    lead = Leads.objects.filter(amo_id=i.get('id')).first()
                    if not lead:
                        lead_id = i.get('id')
                        data = get_leads_data(i, amo_token, lead_id)
                        if data[4]:
                            Leads.objects.create(amo_id=i.get('id'), name=i.get('name'), price=i.get('price'),
                                                 funnel=data[0],
                                                 funnel_status=data[1], created_at=data[2], updated_at=data[3],
                                                 client=data[4])
                        else:
                            Leads.objects.create(amo_id=i.get('id'), name=i.get('name'), price=i.get('price'),
                                                 funnel=data[0],
                                                 funnel_status=data[1], created_at=data[2], updated_at=data[3])
            else:
                if res.get('leads').get('delete'):
                    for i in res.get('leads').get('delete'):
                        Leads.objects.filter(amo_id=i.get('id')).first().delete()

        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksClients(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if self.request.data:
            res = self.request.data
            if res.get('contacts').get('update'):
                for i in res.get('contacts').get('update'):
                    contact = Clients.objects.filter(amo_id=i.get('id')).first()
                    if contact:
                        contact.name = i.get('name')
                        phone = get_contacts_data(i)
                        if phone:
                            contact.phone = phone
                        contact.save()
            elif res.get('contacts').get('add'):
                for i in res.get('contacts').get('add'):
                    contact = Clients.objects.filter(amo_id=i.get('id')).first()
                    if not contact:
                        phone = get_contacts_data(i)
                        Clients.objects.create(amo_id=i.get('id'), name=i.get('name'), phone=phone)
            else:
                if res.get('contacts').get('delete'):
                    for i in res.get('contacts').get('delete'):
                        Clients.objects.filter(amo_id=i.get('id')).first().delete()
        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class WebHooksCustomers(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if self.request.data:
            res = self.request.data
            amo_token = auth_amo_account()
            if res.get('customers').get('update'):
                for i in res.get('customers').get('update'):
                    customer_id = i.get('id')
                    customer = Customers.objects.filter(amo_id=customer_id).first()
                    if customer:
                        customer_custom_fields = i.get('custom_fields_values')
                        user = get_customer_user(customer_custom_fields, customer_id, amo_token)
                        data = get_customer_data(i, amo_token, customer_id)
                        customer.name = i.get('name')
                        if i.get('next_price'):
                            customer.price = i.get('next_price')
                        if data[0]:
                            customer.status = data[0]
                        if i.get('next_date'):
                            next_date = datetime.datetime.utcfromtimestamp(int(i.get('next_date'))).strftime(
                                '%Y-%m-%d %H:%M:%S')
                            customer.next_date = next_date
                        customer.created_at = data[1] if data[1] else None
                        customer.updated_at = data[2] if data[2] else None
                        if user:
                            customer.user = user
                        if data[3]:
                            customer.client = data[3]
                        customer.save()
            elif res.get('customers').get('add'):
                for i in res.get('customers').get('add'):
                    customer = Customers.objects.filter(amo_id=i.get('id')).first()
                    if not customer:
                        customer_id = i.get('id')
                        data = get_customer_data(i, amo_token, customer_id)
                        next_date = datetime.datetime.utcfromtimestamp(int(i.get('next_date'))).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        customer_custom_fields = i.get('custom_fields_values')
                        user = get_customer_user(customer_custom_fields,customer_id, amo_token)

                        cus = Customers.objects.create(amo_id=i.get('id'), name=i.get('name'), price=i.get('next_price'),
                                                       next_date=next_date, created_at=data[1], updated_at=data[2], status=data[0])
                        if data[3]:
                            cus.client = data[3]
                        if user:
                            cus.user = user
                        cus.save()

            else:
                if res.get('customers').get('delete'):
                    for i in res.get('customers').get('delete'):
                        Customers.objects.filter(amo_id=i.get('id')).first().delete()

        return Response({"message": "ok"}, status=status.HTTP_200_OK)
