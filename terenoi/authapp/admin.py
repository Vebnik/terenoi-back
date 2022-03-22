from django.contrib import admin
from authapp.models import User, VoxiAccount, UserStudyLanguage, StudyLanguage
from profileapp.models import ManagerToUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'last_login', 'is_teacher', 'is_student')
    list_filter = ('is_staff', 'is_active')

    def save_model(self, request, obj, form, change):
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
