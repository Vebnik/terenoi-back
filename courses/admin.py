from django.contrib import admin
from django.db.models import Q

from authapp.models import User
from courses.models import Courses, LessonCourse


class LessonCourseInline(admin.TabularInline):
    extra = 1
    model = LessonCourse

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(Q(is_teacher=True) | Q(is_staff=True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)

    inlines = [
        LessonCourseInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(Q(is_teacher=True) | Q(is_staff=True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



# @admin.register(LessonCourse)
# class LessonCourseAdmin(admin.ModelAdmin):
#     list_display = ('course', 'title', 'author')
#     list_filter = ('course', 'author',)
