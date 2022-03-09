from django.contrib import admin

# Register your models here.
from profileapp.models import TeacherSubject, Subject, ReferralPromo, ManagerToUser, UserParents, GlobalUserPurpose, \
    LanguageInterface, Interests, UserInterest


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


@admin.register(UserParents)
class UserParentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'parent_phone', 'parent_email')


@admin.register(GlobalUserPurpose)
class GlobalUserPurposeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')


@admin.register(LanguageInterface)
class LanguageInterfaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'interface_language')


@admin.register(Interests)
class InterestsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user',)
