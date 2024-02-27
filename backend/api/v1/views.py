from ambassadors.models import Ambassador
from rest_framework import viewsets

from .serializers import AmbassadorSerializer


class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer
