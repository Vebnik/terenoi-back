from django.contrib import admin
from django.db import ProgrammingError
from settings.models import ReferralSettings, RateTeachers, DeadlineSettings, CityTimeZone, UserCity, WeekDays, \
    AmoCRMToken


@admin.register(ReferralSettings)
class ReferralSettingsAdmin(admin.ModelAdmin):
    list_display = ('lesson_count', 'amount', 'currency')


@admin.register(RateTeachers)
class RateTeachersAdmin(admin.ModelAdmin):
    list_display = ('subject', 'rate')
    list_filter = ('subject',)


@admin.register(DeadlineSettings)
class DeadlineSettingsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day_count')
    list_filter = ('subject',)


@admin.register(CityTimeZone)
class CityTimeZoneAdmin(admin.ModelAdmin):
    list_display = ('city', 'time_zone')


@admin.register(UserCity)
class UserCityAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


@admin.register(WeekDays)
class WeekDaysAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


@admin.register(AmoCRMToken)
class AmoCRMTokenAdmin(admin.ModelAdmin):
    list_display = ('pk',)
