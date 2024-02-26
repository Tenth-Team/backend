from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AmbassadorViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'ambassadors', AmbassadorViewSet)
router.register(r'content', ContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
