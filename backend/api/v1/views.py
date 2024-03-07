from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ambassadors.choices import GENDER_CHOICES, STATUS_CHOICES
from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
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
from .schemas import content_schema, merch_schema
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorGoalSerializer,
    AmbassadorReadSerializer,
    AmbassadorUpdateSerializer,
    ContentSerializer,
    MerchandiseShippingRequestSerializer,
    PromoCodeSerializer,
    TrainingProgramSerializer,
    YandexFormAmbassadorCreateSerializer,
)


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
        if self.action == 'partial_update':
            return AmbassadorUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def filters(self, request):
        """
        Метод для получения списка фильтров.
        """
        ya_edu_options = [{'id': edu.id, 'name': edu.name} for edu in
                          TrainingProgram.objects.all()]
        country_options = [{'id': country.id, 'name': country.name} for country
                           in Country.objects.all()]
        city_options = [{'id': city.id, 'name': city.name} for city in
                        City.objects.all()]

        filters_data = {
            'ya_edu': {'name': 'Программа обучения', 'values': ya_edu_options},
            'country': {'name': 'Страна', 'values': country_options},
            'city': {'name': 'Город', 'values': city_options},
            'status': {'name': 'Статус амбассадора',
                       'values': [{'id': choice[0], 'name': choice[1]} for
                                  choice in STATUS_CHOICES]},
            'gender': {'name': 'Пол',
                       'values': [{'id': choice[0], 'name': choice[1]} for
                                  choice in GENDER_CHOICES]},
            'order': {'name': 'Сортировать',
                      'values': [
                          {'id': 'date', 'name': 'По дате'},
                          {'id': 'name', 'name': 'По алфавиту'},
                      ]}
        }

        return Response(filters_data)


class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer


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


class AmbassadorGoalView(ListAPIView):
    """
    View для просмотра списка целей амбассадорства.
    """
    queryset = AmbassadorGoal.objects.all()
    serializer_class = AmbassadorGoalSerializer


class TrainingProgramView(ListAPIView):
    """
    View для просмотра списка программ обучения.
    """
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
