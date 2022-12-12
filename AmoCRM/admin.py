from django.contrib import admin

# Register your models here.
from AmoCRM.models import Funnel, FunnelStatus, Clients, Leads, CustomerStatus, Customers


@admin.register(Funnel)
class FunnelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FunnelStatus)
class FunnelStatusAdmin(admin.ModelAdmin):
    list_display = ('funnel', 'name',)


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone')
    search_fields = ['name','amo_id']


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'funnel', 'funnel_status', 'client')
    search_fields = ['name','amo_id']


@admin.register(CustomerStatus)
class CustomerStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'client','user')
    search_fields = ['name','amo_id']
