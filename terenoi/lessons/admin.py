from django.contrib import admin

from lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk','teacher', 'student', 'date', 'lesson_status')
    list_filter = ('lesson_status',)

