from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from ambassadors.models import Ambassador, Content, PromoCode

from .filters import ContentStatusFilter
from .serializers import (
    AmbassadorCreateSerializer,
    AmbassadorReadSerializer,
    ContentSerializer,
    YandexFormAmbassadorCreateSerializer,
    PromoCodeSerializer
)


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorCreateSerializer

    def get_serializer_class(self):
        if self.request.headers.get('X-Source') == 'YandexForm':
            return YandexFormAmbassadorCreateSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return AmbassadorReadSerializer
        return super().get_serializer_class()

class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer


class ContentViewSet(viewsets.ModelViewSet):
    """Viewset для модели Контента
    Позволяет фильтровать выборку по полям status и full_name.
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = ContentStatusFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('full_name',)
