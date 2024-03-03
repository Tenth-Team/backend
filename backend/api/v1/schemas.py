from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
)

from .serializers import ContentSerializer

content_schema = {
    'list': extend_schema(
        summary="Получение списка контента",
        description="Возвращает пагинированный список объектов контента с "
        "возможностью фильтрации по статусу и поиска по имени.",
        parameters=[
            OpenApiParameter(
                name='status',
                description='Статус контента для фильтрации',
                required=False,
                type=str,
                examples=[
                    OpenApiExample("Новая публикация", value="new"),
                    OpenApiExample("Одобрена", value="approved"),
                    OpenApiExample("Не одобрена", value="rejected"),
                ],
            ),
            OpenApiParameter(
                name='search',
                description='Поиск по имени и фамилии',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='limit',
                description='Лимит объектов на странице',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='offset',
                description='Смещение от начала списка',
                required=False,
                type=int,
            ),
        ],
        responses={200: ContentSerializer(many=True)},
    ),
    'create': extend_schema(
        summary="Создание нового объекта контента",
        description="Создает новый объект контента с данными, "
        "предоставленными в запросе.",
        request=ContentSerializer,
        responses={201: ContentSerializer},
        examples=[
            OpenApiExample(
                'Пример создания контента',
                summary='Пример запроса на создание контента',
                value={
                    'full_name': 'Иван Иванов',
                    'telegram': '@ivanivanov',
                    'link': 'http://example.com/content',
                    'guide': True,
                },
                request_only=True,
            ),
            OpenApiExample(
                name='Пример ответа на создание контента',
                value={
                    "id": 1,
                    "full_name": "Иван Иванов",
                    "telegram": "@ivanivanov",
                    "link": "http://example.com/content",
                    "guide": True,
                    "status": "Новая публикация",
                    "created_date": "2024-03-03",
                    "ambassador": 1,
                },
                response_only=True,
                status_codes=['201'],
            ),
        ],
    ),
    'partial_update': extend_schema(
        summary="Частичное обновление объекта контента",
        description="Обновляет часть данных объекта контента с указанным ID. "
        "Использовать для обновления статуса",
        request=ContentSerializer,
        responses={200: ContentSerializer},
        examples=[
            OpenApiExample(
                'Пример обновления статуса контента',
                summary='Пример запроса на создание контента',
                value={
                    'status': 'Не одобрено',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Пример обновления статуса контента',
                summary='Пример ответа на обновления статуса контента',
                value={
                    "id": 1,
                    "full_name": "Иван Иванов",
                    "telegram": "@ivanivanov",
                    "link": "http://example.com/content",
                    "guide": True,
                    "status": "Не одобрено",
                    "created_date": "2024-03-03",
                    "ambassador": 1,
                },
                response_only=True,
                status_codes=['200'],
            ),
        ],
    ),
}
