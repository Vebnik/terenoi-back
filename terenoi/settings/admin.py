from django.contrib import admin
from django.db import ProgrammingError
from settings.models import ReferralSettings, RateTeachers, DeadlineSettings, CityTimeZone


@admin.register(ReferralSettings)
class ReferralSettingsAdmin(admin.ModelAdmin):
    list_display = ('lesson_count', 'amount', 'currency')


@admin.register(RateTeachers)
class RateTeachersAdmin(admin.ModelAdmin):
    list_display = ('subject', 'rate')


@admin.register(DeadlineSettings)
class DeadlineSettingsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day_count')


@admin.register(CityTimeZone)
class CityTimeZoneAdmin(admin.ModelAdmin):
    list_display = ('city', 'time_zone')