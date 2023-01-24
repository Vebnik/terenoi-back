from django import forms
from django.utils.translation import gettext_lazy as _

from manager.mixins import StyleFormMixin
from authapp.models import User

class StudentFilterForm(forms.Form):
  lessons_residue = forms.IntegerField(max_value=10, min_value=0)
  balance_residue = forms.CharField(max_length=9)
  status = forms.CharField(max_length=100)


class StudentSearchForm(StyleFormMixin, forms.Form):
  search_data = forms.CharField(max_length=100)


class StudentCreateForm(forms.ModelForm):

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
      'username',
      )

  