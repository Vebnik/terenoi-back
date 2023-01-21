from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, TemplateView, UpdateView

from authapp.models import User
from .mixins import UserAccessMixin, PagePaginateByMixin
from .forms import StudentSearchForm


class DashboardView(UserAccessMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ''
    template_name = 'manager/dashboard.html'


class UsersStudentListView(UserAccessMixin, PagePaginateByMixin, ListView):
    template_name = 'manager/users.html'
    queryset = User.objects.filter(is_student__exact=True)
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', self.paginate_by)


class UsersStudenSearchtListView(UserAccessMixin, ListView):

    template_name = 'manager/users.html'
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)

    def dispatch(self, request, *args, **kwargs):
        form = StudentSearchForm(request.GET)

        if form.is_valid():

            balance_residue = form.cleaned_data.get('balance_residue').split('-')

            self.queryset = User.objects.filter(
                studentbalance__lessons_balance__gte=int(form.cleaned_data.get('lessons_residue')),
                status=form.cleaned_data.get('status'),
                studentbalance__money_balance__gte=int(balance_residue[0]),
                studentbalance__money_balance__lte=int(balance_residue[1])
            )

        if not self.queryset: self.queryset = []

        return super().dispatch(request, *args, **kwargs)


class UsersTeacherListView(UserAccessMixin, ListView):
    template_name = 'manager/users_teacher.html'
    queryset = User.objects.filter(is_teacher__exact=True)
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 1)


class UsersManagerListView(UserAccessMixin, ListView):    
    template_name = 'manager/users_manager.html'
    queryset = User.objects.filter(is_student__exact=False, is_teacher__exact=False)
    paginate_by = 1

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)


class UsersCreateView(UserAccessMixin, TemplateView):
    template_name = 'manager/users_create.html'
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

