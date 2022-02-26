from django.contrib import admin

# Register your models here.
from profileapp.models import TeacherSubject, Subject, ReferralPromo, ManagerToUser


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(TeacherSubject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')


@admin.register(ReferralPromo)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used')


@admin.register(ManagerToUser)
class ManagerToUserAdmin(admin.ModelAdmin):
    list_display = ('manager', 'user')
