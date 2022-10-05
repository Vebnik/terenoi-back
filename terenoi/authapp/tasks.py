import datetime

import requests

import AmoCRM
from authapp.services import get_students_alfa, get_funnel, get_amo_leads, get_customer_status, add_func_customer, \
    get_amo_customers
from terenoi.celery import app


@app.task
def get_student_alfa_celery(token):
    get_students_alfa(token)


@app.task
def get_leads_amo_celery(token):
    get_amo_leads(token)


@app.task
def get_customers_amo_celery(token):
    get_amo_customers(token)
