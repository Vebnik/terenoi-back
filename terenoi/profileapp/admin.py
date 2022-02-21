from django.contrib import admin

# Register your models here.
from profileapp.models import TeacherSubject, Subject, ReferralPromo


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(TeacherSubject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')


@admin.register(ReferralPromo)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used')
