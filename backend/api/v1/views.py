from django.shortcuts import render
from rest_framework import viewsets
from ambassadors.models import Ambassador
from .serializers import AmbassadorSerializer

class AmbassadorViewSet(viewsets.ModelViewSet):
    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer