from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from django import forms


class UserAccessMixin:

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)


class PagePaginateByMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        self.paginate_by = request.COOKIES.get('paginate_by', 10)
        return super().dispatch(request, *args, **kwargs)


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            elif isinstance(field.widget, forms.widgets.RadioSelect):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

