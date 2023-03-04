from django.forms import formset_factory

from manager.forms import StudentCreateForm, AdditionalUserNumberForm


AdditionalUserNumberFormSet = formset_factory(
  AdditionalUserNumberForm,
  extra=1,
  max_num=1000,
  min_num=0
)


StudentCreateFormSet = formset_factory(
  StudentCreateForm,
  extra=0,
  max_num=1000,
  min_num=1
)

