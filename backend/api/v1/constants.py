SCHEMA_DATE = '2000-01-01'

CONTENT_REQ_EXAMPLE = {
    'full_name': 'Иван Иванов',
    'telegram': '@ivanivanov',
    'link': 'http://example.com/content',
    'guide': True,
}

CONTENT_RESP_EXAMPLE = {
    "id": 1,
    "status": "Новая публикация",
    "created_date": SCHEMA_DATE,
    "ambassador": 1
} | CONTENT_REQ_EXAMPLE

MERCH_REQ_EXAMPLE = {
    "status_send": "Новая заявка",
    "comment": "Комментарий",
    "name_merch": 1,
    "ambassador": 1
}
MERCH_RESP_EXAMPLE = {"id": 1, "created_date": SCHEMA_DATE} | MERCH_REQ_EXAMPLE

PROMO_CODE_REQ_EXAMPLE = {
    "status": "Активный",
    "name": "promo_code",
    "ambassador": 1
}

PROMO_CODE_RESP_EXAMPLE = {"id": 1} | PROMO_CODE_REQ_EXAMPLE
