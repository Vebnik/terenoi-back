from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework, \
    ManagerRequests, Schedule, ScheduleSettings, ManagerRequestsRejectTeacher


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'teacher', 'student', 'date', 'transfer_date', 'schedule', 'lesson_status')
    list_filter = ('lesson_status',)
    search_fields = ['teacher__username', 'teacher__first_name', 'teacher__last_name', 'student__username',
                     'student__first_name', 'student__last_name']
    date_hierarchy = 'date'


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
    list_filter = ('is_resolved', 'type')
    search_fields = ['user__username', 'user__first_name', 'user_last_name', 'manager__username',
                     'manager__first_name', 'manager__last_name']
    date_hierarchy = 'date'

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
    list_display = ('teacher', 'student', 'title', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ['teacher__username', 'teacher__first_name', 'teacher_last_name', 'student__username',
                     'student__first_name', 'student__last_name']

    inlines = [
        ScheduleSettingsInline,
    ]


@admin.register(ManagerRequestsRejectTeacher)
class ManagerRequestsRejectTeacherAdmin(admin.ModelAdmin):
    list_display = ('manager', 'student', 'old_teacher', 'is_resolved', 'account_actions')
    list_filter = ('is_resolved',)
    search_fields = ['student__username', 'student__first_name', 'student__last_name', 'manager__username',
                     'manager__first_name', 'manager__last_name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/accept/',
                self.admin_site.admin_view(self.process_accept),
                name='account-accept_student',
            ),
            path(
                '<int:pk>/reject/',
                self.admin_site.admin_view(self.process_reject),
                name='account-reject_student',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        if not obj.is_resolved:
            return format_html(
                '<a class="button" href="{}">Подтвердить</a> '
                '<a class="button" href="{}">Отклонить</a> ',
                reverse('admin:account-accept_student', args=[obj.pk]),
                reverse('admin:account-reject_student', args=[obj.pk]),
            )

    def process_accept(self, request, pk, *args, **kwargs):
        req = ManagerRequestsRejectTeacher.objects.filter(pk=pk).first()
        req.is_resolved = True
        shedules = Schedule.objects.filter(student=req.student, teacher=req.old_teacher, subject=req.subject)
        if shedules:
            for sh in shedules:
                sh.teacher = req.new_teacher
                sh.save()
        else:
            lessons = Lesson.objects.filter(student=req.student, teacher=req.old_teacher,
                                            subject=req.subject)
            lessons.update(teacher=req.new_teacher)
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def process_reject(self, request, pk, *args, **kwargs):
        req = ManagerRequestsRejectTeacher.objects.filter(pk=pk).first()
        req.is_resolved = True
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
