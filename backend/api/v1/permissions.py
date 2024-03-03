from django.conf import settings
from rest_framework import permissions


class IsAuthenticatedOrYandexForms(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('Authorization')
        return (request.user.is_authenticated
                or request.method == 'POST' and api_key == settings.YANDEX_KEY)
