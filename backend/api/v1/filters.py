from ambassadors.choices import (
    CONTENT_STATUS_CHOICES,
    GENDER_CHOICES,
    STATUS_CHOICES,
)
from ambassadors.models import Ambassador, Content
from django_filters import FilterSet
from django_filters.filters import (
    BaseInFilter,
    CharFilter,
    ChoiceFilter,
    OrderingFilter,
)


class ContentFilter(FilterSet):
    """Класс для фильтрации Контента."""

    status = ChoiceFilter(choices=CONTENT_STATUS_CHOICES)
    full_name = CharFilter(field_name='full_name', lookup_expr='icontains')

    class Meta:
        model = Content
        fields = ['status']
        status_choices = CONTENT_STATUS_CHOICES


class AmbassadorFilter(FilterSet):
    """
    Фильтры для амбассадоров.
    """

    ya_edu = BaseInFilter(field_name='ya_edu', lookup_expr='in')
    country = BaseInFilter(field_name='country', lookup_expr='in')
    city = BaseInFilter(field_name='city', lookup_expr='in')
    status = ChoiceFilter(choices=STATUS_CHOICES)
    gender = ChoiceFilter(choices=GENDER_CHOICES)
    order = OrderingFilter(
        fields=(
            ('reg_date', 'date'),
            ('full_name', 'name'),
        ),
    )

    class Meta:
        model = Ambassador
        fields = []
