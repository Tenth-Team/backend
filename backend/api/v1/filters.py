from ambassadors.choices import CONTENT_STATUS_CHOICES
from ambassadors.models import Content
from django_filters import FilterSet
from django_filters.filters import CharFilter
from rest_framework.exceptions import ValidationError


class UniversalChoiceFilter(CharFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        model = self.parent.Meta.model
        field = model._meta.get_field(self.field_name)
        choices = dict(field.choices)

        if value and value in choices.values():
            reverse_choices = {v: k for k, v in choices.items()}
            value = reverse_choices.get(value)
        else:
            raise ValidationError(
                f"Недопустимое значение для статуса: {value}")

        return super().filter(qs, value)


class BaseStatusFilter(FilterSet):
    status = UniversalChoiceFilter()

    class Meta:
        abstract = True


class StatusFilter(BaseStatusFilter):
    class Meta(BaseStatusFilter.Meta):
        model = Content
        fields = ['status']
        status_choices = CONTENT_STATUS_CHOICES
