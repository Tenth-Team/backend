from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import (
    AmbassadorGoalView,
    AmbassadorViewSet,
    ContentViewSet,
    MerchandiseShippingRequestViewSet,
    PromoCodeViewSet,
    TrainingProgramView,
)

router = DefaultRouter()
router.register(r'ambassadors', AmbassadorViewSet)
router.register(r'content', ContentViewSet)
router.register(r'promocodes', PromoCodeViewSet)
router.register(r'merchandise', MerchandiseShippingRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path('ambassador_goals/', AmbassadorGoalView.as_view(),
         name='ambassador_goals'),
    path('training_programs', TrainingProgramView.as_view(),
         name='training_programs')
]
