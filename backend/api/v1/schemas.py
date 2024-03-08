from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
)

from .constants import (
    AMBASSADOR_REQ_EXAMPLE,
    AMBASSADOR_RESP_EXAMPLE,
    CONTENT_PATCH_EXAMPLE,
    CONTENT_REQ_EXAMPLE,
    CONTENT_RESP_EXAMPLE,
    MERCH_PATCH_EXAMPLE,
    MERCH_REQ_EXAMPLE,
    MERCH_RESP_EXAMPLE,
    PROMO_CODE_REQ_EXAMPLE,
    PROMO_CODE_RESP_EXAMPLE,
)


def get_unique_id_param(name):
    return OpenApiParameter(
        name='id',
        description=f'Уникальный идентификатор {name}',
        required=True,
        location=OpenApiParameter.PATH
    )


ambassador_schema = {
    'retrieve': extend_schema(
        summary='Получение конкретного объекта амбассадора',
        description='Возвращает объект амбассадора, '
                    'по переданному ID в параметре пути.',
        examples=[
            OpenApiExample(
                'retrieve_ambassador_example',
                summary='Пример ответа на получение амбассадора',
                value=AMBASSADOR_RESP_EXAMPLE,
                response_only=True
            )
        ],
        parameters=[get_unique_id_param('амбассадора')]
    ),
    'list': extend_schema(
        summary='Получение списка амбассадоров',
        description='Возвращает пагинированный список объектов амбассадора с '
                    'возможностью фильтрации по городу, стране, гендеру, '
                    'статусу и образовательной программе '
                    'с возможностью применения сортировки.',
        parameters=[
            OpenApiParameter(
                name='status',
                description='Статус контента для фильтрации',
                required=False,
                type=str,
                examples=[
                    OpenApiExample("new", value="new"),
                    OpenApiExample("approved", value="approved"),
                    OpenApiExample("rejected", value="rejected"),
                ],
            ),
            OpenApiParameter(
                name='full_name',
                description='Поиск по имени и фамилии',
                required=False,
                type=str,
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
            OpenApiParameter(
                name='city',
                description='Параметр фильтра по городу(-ам).\n\nНесколько '
                            'значений могут быть разделены запятыми.',
                type=int,
                many=True
            ),
            OpenApiParameter(
                name='country',
                description='Параметр фильтра по стране(-ам).\n\nНесколько '
                            'значений могут быть разделены запятыми.',
                type=int,
                many=True
            ),
            OpenApiParameter(
                name='gender',
                description='Параметр фильтра по полу.',
                enum=[
                    'Мужской', 'Женский'
                ],
            ),
            OpenApiParameter(
                name='ya_edu',
                description='Параметр фильтра по образовательной '
                            'программе(-ам).\n\nНесколько '
                            'значений могут быть разделены запятыми.',
                type=int,
                many=True
            ),
            OpenApiParameter(
                name='status',
                description='Параметр фильтра по статусу.\n\n'
                            '- `active` - активные \n\n'
                            '- `paused` - на паузе\n\n'
                            '- `not_ambassador` - не амбассадор\n\n'
                            '- `pending` - уточняется',
                examples=[
                    OpenApiExample('Активный', value='active'),
                    OpenApiExample('На паузе', value='paused'),
                    OpenApiExample('Не амбассадор', value='not_ambassador'),
                    OpenApiExample('Уточняется', value='pending'),
                ],
            ),
            OpenApiParameter(
                name='order',
                description='Параметр сортировки по дате.\n\n'
                            '- ` date` - по возрастанию даты\n\n'
                            '- `-date` - по убыванию даты\n\n'
                            '- ` name` - по возрастанию имени\n\n'
                            '- `-name` - по убыванию имени',
                enum=[
                    'date', '-date', 'name', '-name'
                ],
                many=True
            ),
        ],
        examples=[
            OpenApiExample(
                name='list_ambassador_example',
                summary='Пример ответа на получение списка амбассадоров',
                value=[AMBASSADOR_RESP_EXAMPLE],
                response_only=True
            )
        ],
    ),
    'create': extend_schema(
        summary='Создание нового объекта амбассадора',
        description='Создает новый объект амбассадора с данными, '
                    'предоставленными в запросе.',
        examples=[
            OpenApiExample(
                name='create_ambassador_example',
                summary='Пример запроса на создание амбассадора',
                value=AMBASSADOR_REQ_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                name='create_ambassador_example',
                summary='Пример ответа на создание амбассадора',
                value=AMBASSADOR_RESP_EXAMPLE,
                response_only=True
            )
        ]
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление объекта амбассадора',
        description='Обновляет часть данных объекта амбассадора с '
                    'указанным ID. \n\n',
        examples=[
            OpenApiExample(
                'patch_ambassador_example',
                summary='Пример запроса на изменение контента',
                value={'address': 'Улица Новая, дом 1'},
                request_only=True,
            ),
            OpenApiExample(
                'patch_ambassador_example',
                summary='Пример ответа на обновления статуса амбассадора',
                value=AMBASSADOR_RESP_EXAMPLE,
                response_only=True,
            ),
        ],
        parameters=[get_unique_id_param('амбассадора')]
    ),
    'destroy': extend_schema(
        summary='Удаление амбассадора',
        description='Удаляет объект существующего амбассадора с указанным ID.',
        parameters=[get_unique_id_param('амбассадора')]
    ),
}

filters_schema = {
    'summary': 'Получение списка фильтров',
    'description': 'Возвращает список объектов фильтра',
    'examples': [
        OpenApiExample(
            'retrieve_filters_example',
            summary='Пример ответа на получение списка фильтров',
            response_only=True,
            value={
                'ya_edu': {
                    'name': 'Программа обучения',
                    'values': [{'id': 1, 'name': 'Пример программы'}]
                },
                'country': {
                    'name': 'Страна',
                    'values': [{'id': 1, 'name': 'Пример страны'}]
                },
                'city': {
                    'name': 'Город',
                    'values': [{'id': 1, 'name': 'Пример города'}]
                },
                'status': {
                    'name': 'Статус амбассадора',
                    'values': [{'id': 'status', 'name': 'Пример статуса'}]
                },
                'gender': {
                    'name': 'Пол',
                    'values': [{'id': 'E', 'name': 'Пример пола'}]
                },
                'order': {
                    'name': 'Сортировать',
                    'values': [
                        {'id': 'example_sort', 'name': 'Пример сортировки'},
                    ]
                }
            }
        )
    ]
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
        ],
        parameters=[get_unique_id_param('контента')]
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
                name='full_name',
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
                'patch_ambassador_example',
                summary='Пример ответа на создание контента',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True,
            ),
        ],
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление объекта контента',
        description='Обновляет часть данных объекта контента с указанным ID. '
                    '\n\nИспользовать для обновления статуса',
        examples=[
            OpenApiExample(
                'patch_content_example',
                summary='Пример запроса на изменение контента',
                value=CONTENT_PATCH_EXAMPLE,
                request_only=True,
            ),
            OpenApiExample(
                'Пример обновления статуса контента',
                summary='Пример ответа на обновления статуса контента',
                value=CONTENT_RESP_EXAMPLE,
                response_only=True,
            ),
        ],
        parameters=[get_unique_id_param('контента')]
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
        ],
        parameters=[get_unique_id_param('промокода')]
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
        ],
        parameters=[get_unique_id_param('промокода')]
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
        parameters=[get_unique_id_param('промокода')]
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
        ],
        parameters=[get_unique_id_param('заявки')]
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
                value=MERCH_PATCH_EXAMPLE,
                request_only=True
            ),
            OpenApiExample(
                'patch_merchandise_example',
                summary='Пример ответа на изменение заявки',
                value=MERCH_RESP_EXAMPLE,
                response_only=True
            ),
        ],
        parameters=[get_unique_id_param('заявки')]
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

goals_schema = {
    'summary': 'Получение списка целей',
    'description': 'Возвращает список объектов целей амбассадоров',
    'examples': [
        OpenApiExample(
            'list_goals_example',
            summary='Пример ответа на получение целей',
            value=[
                {
                    "id": 1,
                    "name": "Пример цели"
                }
            ],
            response_only=True
        )
    ]
}

loyalty_schema = {
    'summary': 'Получение списка амбассадоров в программе лояльности',
    'description': 'Возвращает список объектов амбассадоров '
                   'в программе лояльности.',
    'examples': [
        OpenApiExample(
            'list_loyalty_example',
            summary='Пример ответа на получение амбассадоров',
            value=[
                {
                    "id": 1,
                    "full_name": "Иван Иванов",
                    "content_count": 1,
                    "shipped_merch": "Пример названия мерча"
                }
            ],
            response_only=True,
        )
    ]
}

training_program_schema = {
    'summary': 'Получение списка программ обучения',
    'description': 'Возвращает список объектов программы обучения',
    'examples': [
        OpenApiExample(
            'list_training_program_example',
            summary='Пример ответа на получение программ обучения',
            value=[
                {
                    "id": 1,
                    "name": "Пример программы"
                }
            ],
            response_only=True
        )
    ]
}
