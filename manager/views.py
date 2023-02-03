from django.db.models import Q
from django.http import HttpRequest
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView
from pytils import translit
from django.forms import inlineformset_factory

from authapp.models import AdditionalUserNumber
from authapp.models import User
from manager.forms import StudentFilterForm, StudentSearchForm, StudentCreateForm, AdditionalNumberForm
from manager.mixins import UserAccessMixin, PagePaginateByMixin
from manager.service import Utils


# Dashboard page
class DashboardView(UserAccessMixin, TemplateView):
    permission_required = ''
    template_name = 'manager/dashboard.html'


# Student list
class UsersStudentListView(UserAccessMixin, PagePaginateByMixin, ListView):
    template_name = 'manager/users.html'
    queryset = User.objects.filter(is_student__exact=True)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', self.paginate_by)


class UsersStudenFiltertListView(UserAccessMixin, ListView):

    template_name = 'manager/users.html'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', self.paginate_by)

    def dispatch(self, request, *args, **kwargs):
        self.paginate_by = request.COOKIES.get('paginate_by', 10)
        form = StudentFilterForm(request.GET)

        if form.is_valid():

            print(form.cleaned_data)

            balance_residue = form.cleaned_data.get('balance_residue').split('-')

            self.queryset = User.objects.filter(
                studentbalance__lessons_balance__gte=int(form.cleaned_data.get('lessons_residue')),
                status=form.cleaned_data.get('status'),
                studentbalance__money_balance__gte=int(balance_residue[0]),
                studentbalance__money_balance__lte=int(balance_residue[1])
            )

        if not self.queryset: self.queryset = []

        return super().dispatch(request, *args, **kwargs)


class UsersStudenSearchtListView(UserAccessMixin, ListView):
    template_name = 'manager/users.html'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', self.paginate_by)

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.paginate_by = request.COOKIES.get('paginate_by', 10)
        form = StudentSearchForm(request.GET)

        if form.is_valid():
            trans_search_data = translit.translify(form.cleaned_data.get('search_data'))
            search_data = form.cleaned_data.get('search_data')

            trans_first_name = Q(first_name__icontains=trans_search_data)
            trans_last_name = Q(last_name__icontains=trans_search_data)

            first_name = Q(first_name__icontains=search_data)
            last_name = Q(last_name__icontains=search_data)

            phone = Q(phone__icontains=search_data)
            email = Q(email__icontains=search_data)

            self.queryset = User.objects.filter(
                trans_first_name | trans_last_name | first_name | last_name | phone | email, is_student__exact=True
            )

        if not self.queryset: self.queryset = []

        return super().dispatch(request, *args, **kwargs)


# Teacher list
class UsersTeacherListView(UserAccessMixin, PagePaginateByMixin, ListView):
    template_name = 'manager/users_teacher.html'
    queryset = User.objects.filter(is_teacher__exact=True)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 1)


# Manager list
class UsersManagerListView(UserAccessMixin, PagePaginateByMixin, ListView):    
    template_name = 'manager/users_manager.html'
    queryset = User.objects.filter(is_student__exact=False, is_teacher__exact=False)

    def get_paginate_by(self, queryset):
        return self.request.GET.get('by', 10)


class UserDetailView(UserAccessMixin, DetailView):
    model = User
    template_name = 'manager/users_detail.html'


# Create user
class UsersCreateView(UserAccessMixin, CreateView):
    template_name = 'manager/users_create.html'
    form_class = StudentCreateForm
    model = User
    success_url = reverse_lazy('manager:users')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        AdditionalNumberFormSet = inlineformset_factory(
            self.model, AdditionalUserNumber, form=AdditionalNumberForm, extra=1
        )

        return context

    # TODO Переписать на formset
    # TODO Взять реализацию формы и формсета из isa_day_62
    # FIXME Переделать создание доп формы с номером в соответсвии с формсетом
    # TODO Очистка номера
    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = self.object

        if new_user is None:
            return response

        request_form = dict(self.request.POST)
        phones = request_form.get('phone', [])[1:] # slice first phone
        comments = request_form.get('comments', [])

        if phones and comments:

            bulk = [
                AdditionalUserNumber(
                    user_ref=new_user, 
                    phone=Utils.phone_clener(phones[i]), 
                    comment=comments[i]
                ) for i in range(0, len(phones))
            ]

            AdditionalUserNumber.objects.bulk_create(bulk)
            new_user.additional_number.set(bulk)
            new_user.save()

        return response


class UsersUpdateView(UserAccessMixin, UpdateView):
    model = User
    template_name = 'manager/users_create.html'
    form_class = StudentCreateForm
    success_url = reverse_lazy('manager:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_user = self.object

        if new_user is None:
            return response

        request_form = dict(self.request.POST)
        phones = request_form.get('phone', [])[1:] # slice first phone
        comments = request_form.get('comments', [])

        if phones and comments:

            bulk = [
                AdditionalUserNumber(
                    user_ref=new_user,
                    phone=Utils.phone_clener(phones[i]),
                    comment=comments[i]
                ) for i in range(0, len(phones))
            ]

            AdditionalUserNumber.objects.bulk_create(bulk)
            new_user.additional_number.set(bulk)
            new_user.save()

        return response

