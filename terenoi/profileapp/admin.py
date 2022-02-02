from django.contrib import admin

# Register your models here.
from profileapp.models import TeacherSubject, Subject


@admin.register(Subject)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(TeacherSubject)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')

