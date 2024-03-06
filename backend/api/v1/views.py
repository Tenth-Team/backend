from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, viewsets
from rest_framework.pagination import LimitOffsetPagination

from ambassadors.models import (
    Ambassador,
    Content,
    MerchandiseShippingRequest,
    PromoCode,
)

from .filters import ContentFilter
from .permissions import IsAuthenticatedOrYandexForms
from .schemas import content_schema
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
    ContentSerializer,
    LoyaltyAmbassadorSerializer,
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


class AmbassadorLoyaltyViewSet(generics.ListAPIView):
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
