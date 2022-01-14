from django.contrib import admin

# Register your models here.
from profileapp.models import Subject


@admin.register(Subject)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')