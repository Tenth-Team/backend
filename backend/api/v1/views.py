from rest_framework import viewsets

from ambassadors.models import Ambassador, Content

from .serializers import AmbassadorSerializer, ContentSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
