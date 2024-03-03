from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from ambassadors.models import (
    Ambassador,
    Content,
    MerchandiseShippingRequest,
    PromoCode,
)

from .filters import ContentStatusFilter
from .permissions import IsAuthenticatedOrYandexForms
from .schemas import content_schema
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
    ContentSerializer,
    MerchandiseShippingRequestSerializer,
    PromoCodeSerializer,
    YandexFormAmbassadorCreateSerializer,
)


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorCreateSerializer
    permission_classes = (IsAuthenticatedOrYandexForms,)

    def get_serializer_class(self):
        if self.request.headers.get('X-Source') == 'YandexForm':
            return YandexFormAmbassadorCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return AmbassadorReadSerializer
        return super().get_serializer_class()


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


@extend_schema_view(
    list=extend_schema(
        summary='Получение списка заявок',
        methods=['GET'],
        parameters=[
            OpenApiParameter(
                name='id',
                required=False,
                type=int
            ),
        ],
    ),
    partial_update=extend_schema(
        summary='Обновление статуса заявки',
        methods=['PATCH'],
        request=MerchandiseShippingRequestSerializer,
        responses={200: MerchandiseShippingRequestSerializer},
        parameters=[
            OpenApiParameter(
                name='status_send',
                required=False,
                type=str,
            ),
        ],
    ),
    create=extend_schema(
        summary='Создание новой заявки',
        methods=['POST'],
        request=MerchandiseShippingRequestSerializer,
        responses={200: MerchandiseShippingRequestSerializer},
    ),
)
class MerchandiseShippingRequestViewSet(viewsets.ModelViewSet):
    queryset = MerchandiseShippingRequest.objects.all()
    serializer_class = MerchandiseShippingRequestSerializer
    http_method_names = (
        'get',
        'post',
        'patch',
    )

    """def download(self, request):
        return"""
