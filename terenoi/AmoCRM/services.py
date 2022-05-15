import datetime

import requests
from django.conf import settings

import AmoCRM
import authapp
from AmoCRM.models import Funnel, FunnelStatus, CustomerStatus


def get_amo_contact_leads(token, id, string):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'with': {
            'contacts': True
        }
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/{string}/{id}', headers=headers, params=data)
    if res.json().get('_embedded').get('contacts'):
        id_contacst = res.json().get('_embedded').get('contacts')[0].get('id')
        res_contacts = requests.get(f'{settings.AMO_HOST_NAME}api/v4/contacts/{id_contacst}',
                                    headers=headers)
        data_contacts = res_contacts.json()
        client = AmoCRM.models.Clients.objects.filter(amo_id=int(data_contacts.get('id')))
        if client:
            return client.first()
        else:
            try:
                phone = None
                if data_contacts.get('custom_fields_values')[0].get('field_name') == 'Телефон':
                    phone = data_contacts.get('custom_fields_values')[0].get('values')[0].get('value')
                AmoCRM.models.Clients.objects.create(amo_id=int(data_contacts.get('id')),
                                                     name=data_contacts.get('name'), phone=phone)
            except Exception as ex:
                return None


def get_leads_data(i, amo_token, lead_id):
    client = get_amo_contact_leads(amo_token, lead_id, 'leads')
    funnel = Funnel.objects.filter(id_amo_funnel=i.get('leads[update][0][pipeline_id]')).first()
    funnel_status = FunnelStatus.objects.filter(id_amo_funnel_status=i.get('leads[update][0][status_id]')).first()
    ts = int(i.get('leads[update][0][created_at]'))
    create = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ks = int(i.get('leads[update][0][updated_at]'))
    update = datetime.datetime.utcfromtimestamp(ks).strftime('%Y-%m-%d %H:%M:%S')
    return funnel, funnel_status, create, update, client


def get_contacts_data(i):
    if i.get('contacts[update][0][custom_fields][0][name]') == 'Телефон':
        phone = i.get('contacts[update][0][custom_fields][0][values][0][value]')
        return phone
    return None


def get_customer_user(cus_id, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'with': {
            'contacts': True
        }
    }
    res = requests.get(f'{settings.AMO_HOST_NAME}api/v4/customers/{cus_id}', headers=headers, params=data)
    data = res.json()
    customer_custom_fields = data.get('custom_fields_values')
    user = None
    if customer_custom_fields:
        for i in customer_custom_fields:
            if i.get('field_name') == 'Имя ученика':
                student_name_json = i.get('values')[0].get('value')
                try:
                    student_first_name = student_name_json.split()[:2][1]
                    student_last_name = student_name_json.split()[:2][0]
                    user = authapp.models.User.objects.filter(first_name=student_first_name,
                                                              last_name=student_last_name).first()
                    return user
                except Exception:
                    return None

    return user


def get_customer_data(i, amo_token, customer_id):
    funnel_status = None
    if i.get('customers[update][0][status_id]'):
        funnel_status = CustomerStatus.objects.filter(id_amo=i.get('customers[update][0][status_id]')).first()
    ts = int(i.get('customers[update][0][created_at]'))
    create = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ks = int(i.get('customers[update][0][updated_at]'))
    update = datetime.datetime.utcfromtimestamp(ks).strftime('%Y-%m-%d %H:%M:%S')
    client = get_amo_contact_leads(amo_token, customer_id, 'customers')
    return funnel_status, create, update, client
