from django.contrib import admin

from lessons.models import Lesson, LessonMaterials, LessonHomework


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk','teacher', 'student', 'date', 'lesson_status')
    list_filter = ('lesson_status',)


@admin.register(LessonMaterials)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson','material', 'created_at')
    list_filter = ('lesson',)


@admin.register(LessonHomework)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'homework', 'created_at')
    list_filter = ('lesson',)

