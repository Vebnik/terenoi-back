from django import forms
from django.utils.translation import gettext_lazy as _

from manager.mixins import StyleFormMixin
from authapp.models import User
from authapp.models import AdditionalUserNumber


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
      'birth_date', 
      'gender', 
      'phone', 
      'first_name',
      'last_name',
      'middle_name',
      'email',
      'password',
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