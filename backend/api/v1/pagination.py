from rest_framework.pagination import LimitOffsetPagination


class AmbassadorPagination(LimitOffsetPagination):
    """
    Пагинация для амбассадоров.
    """
    default_limit = 30
    max_limit = 100


class ContentPagination(AmbassadorPagination):
    """
    Пагинация для контента.
    """
    pass
