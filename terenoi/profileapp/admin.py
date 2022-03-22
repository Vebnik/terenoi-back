from django.contrib import admin

# Register your models here.
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html

from authapp.models import User
from profileapp.models import TeacherSubject, Subject, ReferralPromo, ManagerToUser, UserParents, GlobalUserPurpose, \
    LanguageInterface, Interests, UserInterest, ManagerRequestsPassword, AgeLearning, MathSpecializations, \
    EnglishSpecializations, EnglishLevel, TeacherAgeLearning, TeacherMathSpecializations, TeacherEnglishSpecializations, \
    TeacherEnglishLevel


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


@admin.register(ManagerRequestsPassword)
class ManagerRequestsPasswordAdmin(admin.ModelAdmin):
    list_display = ('manager', 'user', 'is_resolved', 'account_actions')
    list_filter = ('is_resolved',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/accept/',
                self.admin_site.admin_view(self.process_accept),
                name='account-accept',
            ),
            path(
                '<int:pk>/reject/',
                self.admin_site.admin_view(self.process_reject),
                name='account-reject',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        if not obj.is_resolved:
            return format_html(
                '<a class="button" href="{}">Подтвердить</a> '
                '<a class="button" href="{}">Отклонить</a> ',
                reverse('admin:account-accept', args=[obj.pk]),
                reverse('admin:account-reject', args=[obj.pk]),
            )

    def process_accept(self, request, pk, *args, **kwargs):
        req = ManagerRequestsPassword.objects.filter(pk=pk).first()
        req.is_resolved = True
        user = User.objects.filter(pk=req.user.pk).first()
        password = make_password(req.new_password)
        user.password = password
        user.save()
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def process_reject(self, request, pk, *args, **kwargs):
        req = ManagerRequestsPassword.objects.filter(pk=pk).first()
        req.is_resolved = True
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@admin.register(AgeLearning)
class AgeLearningAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MathSpecializations)
class MathSpecializationsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EnglishSpecializations)
class EnglishSpecializationsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(EnglishLevel)
class EnglishLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TeacherAgeLearning)
class TeacherAgeLearningAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(TeacherMathSpecializations)
class TeacherMathSpecializationsAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(TeacherEnglishSpecializations)
class TeacherEnglishSpecializationsAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(TeacherEnglishLevel)
class TeacherEnglishLevelAdmin(admin.ModelAdmin):
    list_display = ('user',)
