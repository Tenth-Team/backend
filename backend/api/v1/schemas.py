from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
)

from .constants import (
    CONTENT_REQ_EXAMPLE, CONTENT_RESP_EXAMPLE,
    MERCH_REQ_EXAMPLE, MERCH_RESP_EXAMPLE,
    PROMO_CODE_REQ_EXAMPLE, PROMO_CODE_RESP_EXAMPLE,
)

# TODO: можно сделать функцию на основе extend_schema
#  которая будет генерировать такую доку
#  так как содержание однообразное, а дока не очень расширяема

ambassador_schema = {
    'retrieve': extend_schema(
        summary='Получение конкретного объекта амбассадора',
        description='Возвращает объект амбассадора, '
                    'по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_ambassador_example',
                summary='Пример ответа на получение амбассадора',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
}

content_schema = {
    'retrieve': extend_schema(
        summary='Получение конкретного объекта контента',
        description='Возвращает объект контента, '
                    'по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_content_example',
                summary='Пример ответа на получение контента',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
    'list': extend_schema(
        summary='Получение списка контента',
        description='Возвращает пагинированный список объектов контента с '
                    'возможностью фильтрации по статусу и поиска по имени.',
        parameters=[
            OpenApiParameter(
                name='status',
                description='Статус контента для фильтрации',
                examples=[
                    OpenApiExample('Новая публикация', value='new'),
                    OpenApiExample('Одобрена', value='approved'),
                    OpenApiExample('Не одобрена', value='rejected'),
                ],
            ),
            OpenApiParameter(
                name='search',
                description='Поиск по имени и фамилии',
            ),
            OpenApiParameter(
                name='limit',
                description='Лимит объектов на странице',
                type=int,
            ),
            OpenApiParameter(
                name='offset',
                description='Смещение от начала списка',
                type=int,
            ),
        ],
        examples=[
            OpenApiExample(
                'list_content_example',
                summary='Пример ответа получения списка контента.',
                value=CONTENT_RESP_EXAMPLE,
            )
        ]
    ),
    'create': extend_schema(
        summary='Создание нового объекта контента',
        description='Создает новый объект контента с данными, '
                    'предоставленными в запросе.',
        examples=[
            OpenApiExample(
                'create_content_example',
                summary='Пример запроса на создание контента',
                value=CONTENT_REQ_EXAMPLE,
                request_only=True,
            ),
            OpenApiExample(
                name='Пример ответа на создание контента',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True,
            ),
        ],
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление объекта контента',
        description='Обновляет часть данных объекта контента с указанным ID. '
                    'Использовать для обновления статуса',
        examples=[
            OpenApiExample(
                'patch_content_example',
                summary='Пример запроса на изменение контента',
                value={'status': 'Не одобрено'},
                request_only=True,
            ),
            OpenApiExample(
                'Пример обновления статуса контента',
                summary='Пример ответа на обновления статуса контента',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True,
            ),
        ],
    ),
}

promo_code_schema = {
    'retrieve': extend_schema(
        summary='Получение конкретного промокода',
        description='Возвращает объект промокода, '
                    'по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_promo_example',
                summary='Пример ответа на получение промокода',
                value=PROMO_CODE_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
    'list': extend_schema(
        summary='Получение списка промокодов',
        description='Возвращает полный список объектов промокодов.',
        examples=[
            OpenApiExample(
                'list_promo_example',
                summary='Пример ответа на получение списка промокодов',
                value=[PROMO_CODE_RESP_EXAMPLE],
                response_only=True
            ),
        ]
    ),
    'partial_update': extend_schema(
        summary='Изменение существующего промокода',
        description='Обновляет часть данных объекта промокода с указанным ID.',
        examples=[
            OpenApiExample(
                'patch_promo_example',
                summary='Пример запроса изменения промокода',
                value=PROMO_CODE_REQ_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                'patch_promo_example',
                summary='Пример ответа на изменение промокода',
                value=PROMO_CODE_RESP_EXAMPLE,
                response_only=True
            ),
        ]
    ),
    'create': extend_schema(
        summary='Создание нового промокода',
        description='Создает новый объект промокода с данными, '
                    'предоставленными в запросе.',
        examples=[
            OpenApiExample(
                'create_promo_example',
                summary='Пример запроса на создание промокода',
                value=PROMO_CODE_REQ_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                'create_promo_example',
                summary='Пример ответа на создание промокода',
                value=PROMO_CODE_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
    'destroy': extend_schema(
        summary='Удаление промокода',
        description='Удаляет объект существующего промокода с указанным ID.',
        parameters=[
            OpenApiParameter(
                name='id',
                description='Уникальный идентификатор промокода',
                required=True,
                location='path'
            )
        ]
    ),
}

merch_schema = {
    'retrieve': extend_schema(
        summary='Получение конкретной заявки',
        description='Возвращает объект заявки, '
                    'по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_merchandise_example',
                summary='Пример ответа на получение заявки',
                value=MERCH_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
    'list': extend_schema(
        summary='Получение списка заявок',
        description='Возвращает полный список объектов заявок.',
        examples=[
            OpenApiExample(
                'list_merchandise_example',
                summary='Пример ответа на получение списка заявок',
                value=MERCH_RESP_EXAMPLE,
                response_only=True
            ),
        ]
    ),
    'partial_update': extend_schema(
        summary='Изменение существующей заявки',
        description='Обновляет часть данных объекта заявки с указанным ID.',
        examples=[
            OpenApiExample(
                'patch_merchandise_example',
                summary='Пример запроса изменения заявки',
                value=MERCH_REQ_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                'patch_merchandise_example',
                summary='Пример ответа на изменение заявки',
                value=MERCH_RESP_EXAMPLE,
                response_only=True
            ),
        ]
    ),
    'create': extend_schema(
        summary='Создание новой заявки',
        description='Создает новый объект заявки с данными, '
                    'предоставленными в запросе.',
        examples=[
            OpenApiExample(
                'create_merchandise_example',
                summary='Пример запроса на создание заявки',
                value=MERCH_REQ_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                'create_merchandise_example',
                summary='Пример ответа на создание заявки',
                value=MERCH_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
}
