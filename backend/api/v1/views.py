from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from ambassadors.models import Ambassador, Content

from .filters import ContentStatusFilter
from .serializers import AmbassadorSerializer, ContentSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer


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
