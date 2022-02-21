from django.contrib import admin
from django.db import ProgrammingError
from settings.models import ReferralSettings


@admin.register(ReferralSettings)
class ReferralSettingsAdmin(admin.ModelAdmin):
    list_display = ('lesson_count', 'amount', 'currency')
