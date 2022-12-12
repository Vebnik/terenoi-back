from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView


class UserAccessMixin:

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)


class DashboardView(UserAccessMixin, TemplateView):
    template_name = 'manager/dashboard.html'
