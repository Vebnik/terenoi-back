from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from django.urls import path

from authapp.models import User, VoxiAccount, UserStudyLanguage, StudyLanguage
from authapp.services import generate_password, send_generate_data, auth_alfa_account, get_students_alfa, \
    auth_amo_account, get_amo_leads, get_amo_customers, add_func_customer, get_funnel, get_customer_status
from profileapp.models import ManagerToUser
from settings.models import GeneralContacts


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = "admin/model_change_list.html"
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login', 'is_teacher', 'is_student')
    list_filter = ('is_staff', 'is_teacher', 'is_student', 'is_crm')
    search_fields = ['username', 'first_name', 'last_name']

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        custom_urls = [
            path('import/', self.process_import, name='process_import'),
            path('import-leads/', self.process_import_leads, name='process_import_leads'),
            path('import-customers/', self.process_import_customers, name='process_import_customers'),
        ]
        return custom_urls + urls

    def process_import(self, request):
        token = auth_alfa_account()
        get_students_alfa(token)
        return HttpResponseRedirect("../")

    def process_import_leads(self, request):
        amo_token = auth_amo_account()
        get_funnel(amo_token)
        get_amo_leads(amo_token)
        return HttpResponseRedirect("../")

    def process_import_customers(self, request):
        amo_token = auth_amo_account()
        get_customer_status(amo_token)
        add_func_customer(amo_token)
        get_amo_customers(amo_token)
        return HttpResponseRedirect("../")

    def get_changeform_initial_data(self, request):
        return {'password': 111111111}

    def save_model(self, request, obj, form, change):
        if obj.is_pass_generation:
            gen_password = generate_password()
            obj.password = gen_password
            send_generate_data(obj, gen_password)
            obj.is_pass_generation = False
        super(UserAdmin, self).save_model(request, obj, form, change)
        user = ManagerToUser.objects.filter(user=obj).first()
        if not user:
            ManagerToUser.objects.create(manager=request.user, user=obj)
        super(UserAdmin, self).save_model(request, obj, form, change)


@admin.register(VoxiAccount)
class VoxiAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'voxi_username', 'voxi_display_name')


@admin.register(StudyLanguage)
class StudyLanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserStudyLanguage)
class UserStudyLanguageAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(GeneralContacts)
class GeneralContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'telegram', 'whatsapp')
