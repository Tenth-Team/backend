from rest_framework.pagination import LimitOffsetPagination


class AmbassadorPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 100


class ContentPagination(AmbassadorPagination):
    pass
