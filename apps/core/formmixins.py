import contextlib
from collections import OrderedDict
from functools import reduce
from itertools import chain
from operator import add

from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.forms.utils import ErrorList
from django.utils.html import format_html


class MultiFormMixin:
    form_classes = {}

    def __init__(self, data=None, files=None, *args, **kwargs):
        self.data, self.files = data, files
        kwargs.update(data=data, files=files)
        self.initials = kwargs.pop("initial", None)
        if self.initials is None:
            self.initials = {}
        self.forms = OrderedDict()
        self.crossform_errors = []
        for key, form_class in self.form_classes.items():
            fargs, fkwargs = self.get_form_args_kwargs(key, args, kwargs)
            self.forms[key] = form_class(*fargs, **fkwargs)

    def __str__(self):
        return self.as_table()

    def __getitem__(self, key):
        return self.forms[key]

    def clean(self):
        return self.cleaned_data

    @property
    def errors(self):
        errors = {}
        for form_name in self.forms:
            form = self.forms[form_name]
            for field_name in form.errors:
                errors[form.add_prefix(field_name)] = form.errors[field_name]
        if self.crossform_errors:
            errors[NON_FIELD_ERRORS] = self.crossform_errors
        return errors

    @property
    def fields(self):
        fields = []
        for form_name in self.forms:
            form = self.forms[form_name]
            for field_name in form.fields:
                fields += [form.add_prefix(field_name)]
        return fields

    def __iter__(self):
        return chain.from_iterable(self.forms.values())

    @property
    def is_bound(self):
        return any(form.is_bound for form in self.forms.values())

    @property
    def media(self):
        return reduce(add, (form.media for form in self.forms.values()))

    @property
    def cleaned_data(self):
        return OrderedDict(
            (key, form.cleaned_data)
            for key, form in self.forms.items()
            if form.is_valid()
        )

    def get_form_args_kwargs(self, key, args, kwargs):
        fkwargs = kwargs.copy()
        prefix = kwargs.get("prefix")
        prefix = key if prefix is None else f"{key}__{prefix}"
        fkwargs.update(initial=self.initials.get(key), prefix=prefix)
        return args, fkwargs

    def add_crossform_error(self, e):
        self.crossform_errors.append(e)

    def non_field_errors(self):
        form_errors = (
            form.non_field_errors()
            for form in self.forms.values()
            if hasattr(form, "non_field_errors")
        )
        return ErrorList(chain(self.crossform_errors, *form_errors))

    def hidden_fields(self):
        return [field for field in self if field.is_hidden]

    def visible_fields(self):
        return [field for field in self if not field.is_hidden]

    def is_valid(self):
        forms_valid = all(form.is_valid() for form in self.forms.values())
        try:
            self.cleaned_data = self.clean()
        except ValidationError as e:
            self.add_crossform_error(e)
        return forms_valid and not self.crossform_errors

    def is_multipart(self):
        return any(form.is_multipart() for form in self.forms.values())

    def as_table(self):
        return format_html("".join(form.as_table() for form in self.forms.values()))

    def as_ul(self):
        return format_html("".join(form.as_ul() for form in self.forms.values()))

    def as_p(self):
        return format_html("".join(form.as_p() for form in self.forms.values()))

    @cleaned_data.setter
    def cleaned_data(self, data):
        for key, value in data.items():
            child_form = self[key]
            if isinstance(child_form, BaseFormSet):
                for formlet, formlet_data in zip(child_form.forms, value, strict=True):
                    formlet.cleaned_data = formlet_data
            else:
                child_form.cleaned_data = value


class MultiModelForm(MultiFormMixin):
    def __init__(self, *args, **kwargs):
        self.instances = kwargs.pop("instance", None)
        if self.instances is None:
            self.instances = {}
        super().__init__(*args, **kwargs)

    def get_form_args_kwargs(self, key, args, kwargs):
        fargs, fkwargs = super().get_form_args_kwargs(key, args, kwargs)
        with contextlib.suppress(KeyError):
            fkwargs["instance"] = self.instances[key]
        return fargs, fkwargs

    def save(self, *, commit=True):
        objects = OrderedDict(
            (key, form.save(commit)) for key, form in self.forms.items()
        )
        if any(hasattr(form, "save_m2m") for form in self.forms.values()):

            def save_m2m():
                for form in self.forms.values():
                    if hasattr(form, "save_m2m"):
                        form.save_m2m()

            self.save_m2m = save_m2m
        return objects
