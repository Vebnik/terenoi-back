from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView, View
from pytils import translit
from django.forms import inlineformset_factory
import json

from authapp.models import AdditionalUserNumber
from authapp.models import User, Group
from manager.forms import (
    StudentFilterForm, 
    StudentSearchForm, 
    StudentCreateForm, 
    AdditionalNumberForm, 
    SubscriptionForm,
    ScheduleForm,
    )
from manager.mixins import UserAccessMixin, PagePaginateByMixin
from manager.service import Utils
from profileapp.models import ManagerToUser
from finance.models import StudentSubscription, PaymentMethod
from lessons.models import Schedule, ScheduleSettings, Lesson
from settings.models import WeekDays
from profileapp.models import Subject


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
        user: User = context.get('object')

        try:
            manager = ManagerToUser.objects.get(user=kwargs.get('object'))
        except Exception as ex:
            manager = False

        try:
            subscription = user.studentsubscription_set.get(is_active=True)
            context['subscription'] = subscription
            subscription_form = SubscriptionForm(instance=subscription)
        except Exception as ex:
            subscription_form = SubscriptionForm()

        try:
            schedule_settings: ScheduleSettings = \
                user.group_students.first().schedule_group.get(is_completed=False).schedulesettings_set.first()
            context['schedule'] = schedule_settings
            schedule: Schedule = schedule_settings.shedule
            schedule_form = ScheduleForm(instance=schedule, initial={ **schedule_settings.__dict__ })

            context['schedule_settings'] = {
                'lesson_start': schedule_settings.near_lesson.time(),
                'date_start': schedule_settings.near_lesson.date().strftime('%Y-%m-%d'),
            }
        except Exception as ex:
            schedule_form = ScheduleForm()

        context['subscription_form'] = subscription_form
        context['schedule_form'] = schedule_form
        context['manager'] = manager
        context['payment_methods'] = PaymentMethod.objects.all()

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

        m2u = ManagerToUser(user=self.object, manager=self.request.user)
        m2u.save()

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

        if manager and not ManagerToUser.objects.filter(user=self.object, manager=manager):
            m2u = ManagerToUser(user=self.object, manager=manager)
            m2u.save()

        if formset.is_valid():
            formset.instance = self.object
            additional_number = formset.save()
            self.object.additional_user_number.set(additional_number)

        self.object.save()

        return super().form_valid(form)


class SubscriptionCreateView(UserAccessMixin, CreateView):
    model = StudentSubscription
    form_class = SubscriptionForm
    success_url = reverse_lazy('manager:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        pk = self.request.POST.dict().get('pk')
        select_method_pk = self.request.POST.dict().get('payment_method')

        if form.is_valid():
            user = User.objects.get(pk=pk)
            method = PaymentMethod.objects.get(pk=select_method_pk)
            method.save()

            self.object.student = user
            self.object.payment_methods = method
            user.subscription.add(self.object)

            self.object.save()
            user.save()

        return response


class SubscriptionUpdateView(UserAccessMixin, UpdateView):
    model = StudentSubscription
    form_class = SubscriptionForm
    success_url = reverse_lazy('manager:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        pk = self.request.POST.dict().get('pk')
        select_method_pk = self.request.POST.dict().get('payment_method')

        if form.is_valid():
            user = User.objects.get(pk=pk)
            method = PaymentMethod.objects.get(pk=select_method_pk)
            method.save()

            if self.object.payment_methods.pk != method.pk:
                self.object.payment_methods = method

            self.object.student = user
            user.subscription = self.object

            self.object.save()
            user.save()

        return response


class ScheduleCreateView(UserAccessMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('manager:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        form_data = self.request.POST.dict()

        user = User.objects.get(pk=form_data.get('pk'))
        count = int(form_data.get('count'))

        if form.is_valid():

            if not self.object.group:
                start_datetime = Utils.serialize_date(form_data)
            else:
                start_datetime = Utils.serialize_date(form_data)

            if not self.object.group:
                group = Group(
                    title=form_data.get('group_name', f'user-{user.pk}'),
                    description=f"Group for user user-{user.pk}",
                )

            group.save()

            if not self.object.group:
                group.students.set([user])
            else:
                group.students.add([user])

            group.save()
            
            if not self.object.group:
                shedule_setting = ScheduleSettings(
                    shedule=self.object,
                    near_lesson=start_datetime,
                    count=count,
                    lesson_duration=form_data.get('lesson_duration'),
                )
            else:
                shedule_setting = self.object.group.students.first().schedule

            self.object.group = group
            self.object.title = f'user-{user.pk}'
            self.object.save()

            shedule_setting.save()
            user.schedule.add(shedule_setting)

            user.save()
            self.object.save()
    
        return response


class ScheduleUpdateView(UserAccessMixin, UpdateView):
    template_name = 'manager/users_detail.html'
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('manager:users')
        
    def form_valid(self, form):
        response = super().form_valid(form)
        form_data = self.request.POST.dict()

        user = User.objects.get(pk=form_data.get('pk'))
        start_datetime = Utils.serialize_date(form_data)
        count = int(form_data.get('count'))
        lesson_duration = form_data.get('lesson_duration')


        if form.is_valid():                    
            # TODO Обновелние старого ScheduleSettings

            user.schedule.lesson_duration = lesson_duration
            user.schedule.count = count
            user.schedule.near_lesson = start_datetime
            user.schedule.shedule = self.object

            self.object.save()
            user.schedule.save()
            user.save()
    
        return response
    

class ScheduleGetTecherView(UserAccessMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
        
            queryset = None

            for key, value in request.GET.dict().items():
                if key == 'date' and value:
                    date = Utils.normalize_date(value)
                    if queryset is not None: queryset = queryset.filter(date__date=date)
                    else: queryset = Lesson.objects.filter(date__date=date)
                if key == 'subject' and value:
                    if queryset is not None: queryset = queryset.distinct().filter(subject=Subject.objects.get(pk=value))
                    else: queryset = Lesson.objects.distinct().filter(subject=Subject.objects.get(pk=value))
                if key == 'time' and value:
                    time = Utils.normalize_time(value)
                    if queryset is not None: queryset = queryset.filter(date__time=time)
                    else: queryset = Lesson.objects.filter(date__time=time)
                if key == 'weekday' and value:
                    value = [*map(lambda el: el-1 if el>0 else el, map(int, value.split(',')))]       
                    weekdays = [WeekDays.objects.get(number=day_num) for day_num in value]
                    if queryset is not None: queryset = queryset.distinct().filter(schedule__weekday__in=weekdays)
                    else: queryset = Lesson.objects.distinct().filter(schedule__weekday__in=weekdays)
            try:
                teachers = [{
                    'pk': item.teacher.pk, 
                    'fullname': item.teacher.get_full_name(),
                    'group_pk': item.group.pk,
                    'group_name': item.group.title,
                    } for item in queryset]
                return JsonResponse({'data': teachers})
            except Exception as ex:
                return JsonResponse({'data': [], 'error': ex})
