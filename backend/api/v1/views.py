from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ambassadors.models import Ambassador, Content
from rest_framework.pagination import LimitOffsetPagination

from .filters import StatusFilter
from .serializers import AmbassadorSerializer, ContentSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = StatusFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('full_name',)
