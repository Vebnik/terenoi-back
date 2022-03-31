from django.contrib import admin
from django import forms

from authapp.models import User, VoxiAccount, UserStudyLanguage, StudyLanguage
from authapp.services import generatePassword, send_generate_data
from profileapp.models import ManagerToUser
from settings.models import GeneralContacts


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login', 'is_teacher', 'is_student')
    list_filter = ('is_staff', 'is_teacher', 'is_student')
    search_fields = ['username', 'first_name', 'last_name']

    def get_changeform_initial_data(self, request):
        return {'password': 111111111}

    def save_model(self, request, obj, form, change):
        if obj.is_pass_generation:
            gen_password = generatePassword()
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
