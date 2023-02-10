from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from authapp.models import User
from courses.models import Courses, LessonCourse, CourseWishList, PurchasedCourses, PurchasedCoursesRequest, \
    CourseLikeList


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


@admin.register(CourseWishList)
class CourseWishListAdmin(admin.ModelAdmin):
    list_display = ('course', 'user')


@admin.register(CourseLikeList)
class CourseLikeListAdmin(admin.ModelAdmin):
    list_display = ('course', 'user')


@admin.register(PurchasedCourses)
class PurchasedCoursesAdmin(admin.ModelAdmin):
    list_display = ('course', 'user')


@admin.register(PurchasedCoursesRequest)
class PurchasedCoursesRequestAdmin(admin.ModelAdmin):
    list_display = ('course', 'manager', 'user', 'is_resolved', 'account_actions')
    list_filter = ('is_resolved',)
    search_fields = ['course', 'manager__username', 'manager__first_name', 'manager__last_name']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/accept/',
                self.admin_site.admin_view(self.process_accept),
                name='account-accept_course',
            ),
            path(
                '<int:pk>/reject/',
                self.admin_site.admin_view(self.process_reject),
                name='account-reject_course',
            ),
        ]
        return custom_urls + urls

    def account_actions(self, obj):
        if not obj.is_resolved:
            return format_html(
                '<a class="button" href="{}">Подтвердить</a> '
                '<a class="button" href="{}">Отклонить</a> ',
                reverse('admin:account-accept_course', args=[obj.pk]),
                reverse('admin:account-reject_course', args=[obj.pk]),
            )

    def process_accept(self, request, pk, *args, **kwargs):
        req = PurchasedCoursesRequest.objects.filter(pk=pk).first()
        req.is_resolved = True
        PurchasedCourses.objects.get_or_create(user=req.user, course=req.course)
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def process_reject(self, request, pk, *args, **kwargs):
        req = PurchasedCoursesRequest.objects.filter(pk=pk).first()
        req.is_resolved = True
        req.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
