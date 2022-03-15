from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework, \
    ManagerRequests, Schedule, ScheduleSettings


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'teacher', 'student', 'date', 'transfer_date', 'lesson_status')
    list_filter = ('lesson_status',)


@admin.register(LessonMaterials)
class LessonMaterialsAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'material', 'created_at')
    list_filter = ('lesson',)


@admin.register(LessonHomework)
class LessonHomeworkAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'homework', 'created_at')
    list_filter = ('lesson',)


@admin.register(VoximplantRecordLesson)
class VoximplantRecordLessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'session_id')


@admin.register(LessonRateHomework)
class LessonRateHomeworkAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'rate')
    list_filter = ('rate',)


@admin.register(ManagerRequests)
class ManagerRequestsAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'manager', 'user', 'type', 'date', 'is_resolved', 'account_actions')
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
        req = ManagerRequests.objects.filter(pk=pk).first()
        req.is_resolved = True
        if req.type == ManagerRequests.REQUEST_RESCHEDULED:
            req.lesson.lesson_status = Lesson.RESCHEDULED
            req.type = ManagerRequests.RESCHEDULED
            Lesson.objects.create(teacher=req.lesson.teacher, student=req.lesson.student, topic=req.lesson.topic,
                                  subject=req.lesson.subject,
                                  date=req.date)
        else:
            req.lesson.lesson_status = Lesson.CANCEL
            req.type = ManagerRequests.CANCEL
        req.save()
        req.lesson.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def process_reject(self, request, pk, *args, **kwargs):
        req = ManagerRequests.objects.filter(pk=pk).first()
        req.is_resolved = True
        req.type = ManagerRequests.REJECT
        req.lesson.lesson_status = Lesson.SCHEDULED
        req.lesson.transfer_date = None
        req.save()
        req.lesson.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ScheduleSettingsInline(admin.TabularInline):
    model = ScheduleSettings


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'title')

    inlines = [
        ScheduleSettingsInline,
    ]
