from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AmbassadorViewSet
router = DefaultRouter()
router.register(r'ambassadors', AmbassadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
