from django.urls import path

from AmoCRM.views import WebHooksLeads, WebHooksClients, WebHooksCustomers

app_name = 'AmoCRM'

urlpatterns = [
    path('webhooks-leads/', WebHooksLeads.as_view(), name='webhooks_leads'),
    path('webhooks-clients/', WebHooksClients.as_view(), name='webhooks_clients'),
    path('webhooks-customers/', WebHooksCustomers.as_view(), name='webhooks_customers'),

]
