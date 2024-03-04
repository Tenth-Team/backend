from rest_framework.pagination import LimitOffsetPagination


class AmbassadorPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 100