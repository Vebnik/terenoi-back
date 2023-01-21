from django import forms


class StudentFilterForm(forms.Form):
  csrfmiddlewaretoken = forms.CharField(max_length=128)
  lessons_residue = forms.IntegerField(max_value=10, min_value=1)
  balance_residue = forms.CharField(max_length=9)
  status = forms.CharField(max_length=100)


class StudentSearchForm(forms.Form):
  csrfmiddlewaretoken = forms.CharField(max_length=128)
  search_data = forms.CharField(max_length=100)
