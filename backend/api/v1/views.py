from django.utils import timezone
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
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import AmbassadorFilter, ContentFilter
from .pagination import AmbassadorPagination
from .permissions import IsAuthenticatedOrYandexForms
from .schemas import (
    ambassador_schema,
    content_schema,
    filters_schema,
    goals_schema,
    loyalty_schema,
    merch_schema,
    promo_code_schema,
    training_program_schema,
)
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorGoalSerializer,
    AmbassadorReadSerializer,
    AmbassadorUpdateSerializer,
    ContentSerializer,
    LoyaltyAmbassadorSerializer,
    MerchandiseShippingRequestSerializer,
    PromoCodeSerializer,
    TrainingProgramSerializer,
    YandexFormAmbassadorCreateSerializer,
)
from .utils import ExcelRender


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(**ambassador_schema)
class AmbassadorViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для амбассадоров.
    """

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

    def get_queryset(self):
        match self.action:
            case 'list' | 'retrieve':
                active_promocodes = PromoCode.objects.filter(status='active')
                prefetch_active_promocodes = Prefetch(
                    'promo_code', queryset=active_promocodes,
                    to_attr='prefetched_promo_codes'
                )

                return Ambassador.objects.select_related(
                    'ya_edu', 'country', 'city'
                ).prefetch_related(
                    'amb_goals', 'content', prefetch_active_promocodes
                )
            case _:
                return Ambassador.objects.all()

    @extend_schema(**filters_schema)
    @action(detail=False, methods=['get'])
    def filters(self, request):
        """
        Метод для получения списка фильтров.
        """
        ya_edu_options = [
            {'id': edu.id, 'name': edu.name}
            for edu in TrainingProgram.objects.all()
        ]
        country_options = [
            {'id': country.id, 'name': country.name}
            for country in Country.objects.all()
        ]
        city_options = [
            {'id': city.id, 'name': city.name} for city in City.objects.all()
        ]

        filters_data = {
            'ya_edu': {
                'name': 'Программа обучения',
                'type': 'checkbox',
                'values': ya_edu_options
            },
            'country': {
                'name': 'Страна',
                'type': 'checkbox',
                'values': country_options
            },
            'city': {
                'name': 'Город',
                'type': 'checkbox',
                'values': city_options
            },
            'status': {
                'name': 'Статус амбассадора',
                'type': 'select',
                'values': [
                    {'id': choice[0], 'name': choice[1]}
                    for choice in STATUS_CHOICES
                ],
            },
            'gender': {
                'name': 'Пол',
                'type': 'select',
                'values': [
                    {'id': choice[0], 'name': choice[1]}
                    for choice in GENDER_CHOICES
                ],
            },
            'order': {
                'name': 'Сортировать',
                'type': 'select',
                'values': [
                    {'id': 'date', 'name': 'По дате'},
                    {'id': 'name', 'name': 'По алфавиту'},
                ],
            },
        }

        return Response(filters_data)


@extend_schema(tags=["Промокоды"])
@extend_schema_view(**promo_code_schema)
class PromoCodeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели промокода.
    """
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

    queryset = Content.objects.select_related('ambassador')
    serializer_class = ContentSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = ContentFilter
    filter_backends = (DjangoFilterBackend,)
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
    http_method_names = (
        'get',
        'post',
        'patch',
    )

    @action(detail=False, methods=["get"], renderer_classes=[ExcelRender])
    def download(self, request):
        queryset = self.get_queryset()
        now = timezone.now()
        file_name = f'merch_data_{now:%Y-%m-%d_%H-%M-%S}.{request.accepted_renderer.format}'
        serializer = MerchandiseShippingRequestSerializer(queryset, many=True)
        return Response(
            serializer.data,
            headers={"Content-Disposition":
                     f'attachment; filename="{file_name}"'}
        )

@extend_schema(tags=["Программы и цели"], **loyalty_schema)
class AmbassadorLoyaltyViewSet(ListAPIView):
    """Viewset для получения данных для страницы лояльности.
    Возвращает список амбассадоров."""

    shipped_merch_prefetch = Prefetch(
        'merch_shipping_requests',
        queryset=MerchandiseShippingRequest.objects.select_related(
            'name_merch'
        ).filter(status_send='sent_to_logisticians'),
        to_attr='shipped_merch_prefetch',
    )
    content_prefetch = Prefetch(
        'content',
        queryset=Content.objects.filter(status='approved'),
        to_attr='content_prefetch',
    )
    queryset = Ambassador.objects.prefetch_related(
        content_prefetch, shipped_merch_prefetch
    )
    serializer_class = LoyaltyAmbassadorSerializer


@extend_schema(tags=["Программы и цели"], **goals_schema)
class AmbassadorGoalView(ListAPIView):
    """
    View для просмотра списка целей амбассадорства.
    """
    queryset = AmbassadorGoal.objects.all()
    serializer_class = AmbassadorGoalSerializer


@extend_schema(tags=["Программы и цели"], **training_program_schema)
class TrainingProgramView(ListAPIView):
    """
    View для просмотра списка программ обучения.
    """
    queryset = TrainingProgram.objects.all()
    serializer_class = TrainingProgramSerializer
