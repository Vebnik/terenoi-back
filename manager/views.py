from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, TemplateView

from .models import Student

class UserAccessMixin:

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)


class DashboardView(UserAccessMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ''
    template_name = 'manager/dashboard.html'


class UsersListView(ListView):
    template_name = 'manager/users.html'
    model = Student
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)


#TODO переименовать модель Student в USER
class UsersTeacherListView(ListView):
    template_name = 'manager/users_teacher.html'
    model = Student
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)


class UsersManagerListView(ListView):
    template_name = 'manager/users_manager.html'
    model = Student
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)


class UsersCreateView(TemplateView):
    template_name = 'manager/users_create.html'