from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ambassadors.choices import GENDER_CHOICES, STATUS_CHOICES
from ambassadors.models import (
    Ambassador,
    City,
    Content,
    Country,
    MerchandiseShippingRequest,
    PromoCode,
    TrainingProgram,
)

from .filters import AmbassadorFilter, ContentStatusFilter
from .pagination import AmbassadorPagination
from .permissions import IsAuthenticatedOrYandexForms
from .schemas import (
    content_schema, merch_schema, promo_code_schema,
    ambassador_schema, filters_schema,
)
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
    ContentSerializer,
    MerchandiseShippingRequestSerializer,
    PromoCodeSerializer,
    YandexFormAmbassadorCreateSerializer,
)


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(**ambassador_schema)
class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для амбассадоров.
    """
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorCreateSerializer
    pagination_class = AmbassadorPagination
    permission_classes = (IsAuthenticatedOrYandexForms,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AmbassadorFilter

    def get_serializer_class(self):
        if self.request.headers.get('X-Source') == 'YandexForm':
            return YandexFormAmbassadorCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return AmbassadorReadSerializer
        return super().get_serializer_class()

    @extend_schema(**filters_schema)
    @action(detail=False, methods=['get'])
    def filters(self, request):
        """
        Метод для получения списка фильтров.
        """
        filters_data = {
            'ya_edu': {
                'name': 'Программа обучения',
                'values': [{'id': edu.id, 'name': edu.name}
                           for edu in TrainingProgram.objects.all()]
            },
            'country': {
                'name': 'Страна',
                'values': [{'id': country.id, 'name': country.name}
                           for country in Country.objects.all()]
            },
            'city': {
                'name': 'Город',
                'values': [{'id': city.id, 'name': city.name}
                           for city in City.objects.all()]
            },
            'status': {
                'name': 'Статус амбассадора',
                'values': [{'id': choice[0], 'name': choice[1]}
                           for choice in STATUS_CHOICES]
            },
            'gender': {
                'name': 'Пол',
                'values': [{'id': choice[0], 'name': choice[1]}
                           for choice in GENDER_CHOICES]
            },
            'order': {
                'name': 'Сортировать',
                'values': [
                    {'id': 'reg_date', 'name': 'По дате'},
                    {'id': 'full_name', 'name': 'По алфавиту'},
                ]
            }
        }

        return Response(filters_data)


@extend_schema(tags=["Промокоды"])
@extend_schema_view(**promo_code_schema)
class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    http_method_names = (
        'get',
        'post',
        'patch',
        'delete'
    )


@extend_schema(tags=["Контент"])
@extend_schema_view(**content_schema)
class ContentViewSet(viewsets.ModelViewSet):
    """
    Viewset для модели Контента
    Позволяет фильтровать выборку по полям status и full_name.
    """

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = ContentStatusFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('full_name',)
    http_method_names = (
        'get',
        'post',
        'patch',
    )


@extend_schema(tags=["Заявки"])
@extend_schema_view(**merch_schema)
class MerchandiseShippingRequestViewSet(viewsets.ModelViewSet):
    queryset = MerchandiseShippingRequest.objects.all()
    serializer_class = MerchandiseShippingRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = (
        'get',
        'post',
        'patch',
    )

    """def download(self, request):
        return"""
