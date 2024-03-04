from django_filters import FilterSet
from django_filters.filters import CharFilter, ChoiceFilter

from ambassadors.choices import CONTENT_STATUS_CHOICES
from ambassadors.models import Content


class ContentFilter(FilterSet):
    """Класс для фильтрации Контента."""

    status = ChoiceFilter(choices=CONTENT_STATUS_CHOICES)
    full_name = CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = Content
        fields = []
