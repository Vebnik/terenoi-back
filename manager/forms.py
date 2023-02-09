from django import forms
from django.utils.translation import gettext_lazy as _

from manager.mixins import StyleFormMixin

from authapp.models import User
from authapp.models import AdditionalUserNumber

from finance.models import StudentSubscription

from lessons.models import Schedule


class StudentFilterForm(forms.Form):
  lessons_residue = forms.IntegerField(max_value=10, min_value=0)
  balance_residue = forms.CharField(max_length=9)
  status = forms.CharField(max_length=100)


class StudentSearchForm(StyleFormMixin, forms.Form):
  search_data = forms.CharField(max_length=100)


class StudentCreateForm(StyleFormMixin, forms.ModelForm):

  template_name = 'manager/forms/user_create_form.html'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  class Meta:
    model = User
    fields = (
      'avatar',
      'birth_date', 
      'gender', 
      'phone', 
      'first_name',
      'last_name',
      'middle_name',
      'email',
      'password',
      'is_pass_generation'
      )

    widgets = {
      'birth_date': forms.DateInput(attrs={'type': 'date'}),
      'password': forms.TextInput(attrs={'type': 'password'})
    }

  
class AdditionalNumberForm(StyleFormMixin, forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    for key in self.fields:
      self.fields[key].required = True

  class Meta:
    model = AdditionalUserNumber
    fields = ('phone', 'comment')


class SubscriptionForm(StyleFormMixin, forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # self.fields['billing'].widget.attrs['class'] = 'form-check-input'
    self.fields['plan_type'].widget.attrs['class'] = 'form-control form-select'
    self.fields['title'].widget.attrs['placeholder'] = 'Напиример, Стандарт'
    self.fields['lesson_count'].widget.attrs['placeholder'] = 'Например, 8'
    self.fields['lesson_duration'].widget.attrs['placeholder'] = 'Например, 60'
    self.fields['lesson_cost'].widget.attrs['placeholder'] = 'Например, 3000'
    self.fields['subscription_cost'].widget.attrs['placeholder'] = 'Например, 60'

  class Meta:
    model = StudentSubscription
    fields = '__all__'
    exclude = ('student', 'payment_methods', )


class ScheduleForm(StyleFormMixin, forms.ModelForm):

  class Meta:
    model = Schedule
    fields = '__all__'