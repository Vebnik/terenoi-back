from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView
from pytils import translit
from django.forms import inlineformset_factory

from authapp.models import AdditionalUserNumber
from authapp.models import User

from manager.forms import StudentFilterForm, StudentSearchForm, StudentCreateForm, AdditionalNumberForm
from manager.mixins import UserAccessMixin, PagePaginateByMixin

from profileapp.models import ManagerToUser


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # FIXME code smell Nikita
        try: manager = ManagerToUser.objects.get(user=kwargs.get('object'))
        except Exception: manager = False

        context['manager'] = manager
        return context

    def post(self, *args, **kwargs):
        status = self.request.POST.dict().get('status')
        user = self.get_object()

        if user.valid_status(status):
            user.status = status
            user.save()

        return HttpResponseRedirect(reverse_lazy('manager:users_detail', kwargs={'pk': kwargs.get('pk')}))


# Create user
class UsersCreateView(UserAccessMixin, CreateView):
    template_name = 'manager/users_create.html'
    form_class = StudentCreateForm
    model = User
    success_url = reverse_lazy('manager:users')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        AdditionalNumberFormSet = inlineformset_factory(
            self.model, AdditionalUserNumber, form=AdditionalNumberForm, extra=0
        )

        if self.request.method == 'POST':
            formset = AdditionalNumberFormSet(self.request.POST, instance=self.object)
        else:
            formset = AdditionalNumberFormSet(instance=self.object)

        context['formset'] = formset
        return context

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            additional_number = formset.save()
            self.object.additional_user_number.set(additional_number)

        self.object.save()

        return super().form_valid(form)


class UsersUpdateView(UserAccessMixin, UpdateView):
    model = User
    template_name = 'manager/users_create.html'
    form_class = StudentCreateForm
    success_url = reverse_lazy('manager:users')


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        AdditionalNumberFormSet = inlineformset_factory(
            self.model, AdditionalUserNumber, form=AdditionalNumberForm, extra=0
        )

        if self.request.method == 'POST':
            formset = AdditionalNumberFormSet(self.request.POST, instance=self.object)
        else:
            formset = AdditionalNumberFormSet(instance=self.object)

        context['formset'] = formset
        return context


    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            additional_number = formset.save()
            self.object.additional_user_number.set(additional_number)

        self.object.save()

        return super().form_valid(form)


class UsersManagerUpdateView(UserAccessMixin, UpdateView):
    model = User
    template_name = 'manager/user_update_manager.html'
    form_class = StudentCreateForm
    success_url = reverse_lazy('manager:users')

    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy('manager:users_detail', kwargs={'pk': kwargs.get('pk')})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        AdditionalNumberFormSet = inlineformset_factory(
            self.model, AdditionalUserNumber, form=AdditionalNumberForm, extra=0
        )

        if self.request.method == 'POST':
            formset = AdditionalNumberFormSet(self.request.POST, instance=self.object)
        else:
            formset = AdditionalNumberFormSet(instance=self.object)

        context['formset'] = formset
        context['managers'] = User.objects.filter(is_staff=True)

        return context


    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        manager_pk = self.request.POST.dict().get('manager')
        manager = User.objects.get(pk=manager_pk)
        
        self.object = form.save()

        if manager:
            m2u = ManagerToUser(user=self.object, manager=manager)
            m2u.save()

        if formset.is_valid():
            formset.instance = self.object
            additional_number = formset.save()
            self.object.additional_user_number.set(additional_number)

        self.object.save()

        return super().form_valid(form)
