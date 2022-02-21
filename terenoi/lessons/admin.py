from django.contrib import admin

from lessons.models import Lesson, LessonMaterials, LessonHomework, VoximplantRecordLesson, LessonRateHomework


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'teacher', 'student', 'date', 'lesson_status')
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
