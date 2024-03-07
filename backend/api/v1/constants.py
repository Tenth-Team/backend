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

AMBASSADOR_REQ_EXAMPLE = {
    "city": "Москва",
    "country": "Россия",
    "full_name": "Иван Иванов",
    "gender": "М",
    "address": "Улица Пример, дом пример",
    "postal_code": "000000",
    "email": "ivanovivan@example.com",
    "phone_number": "+79999999",
    "telegram": "@ivanovivan",
    "edu": "Высшее",
    "work": "ООО \"Пример\"",
    "study_goal": "Пример цели",
    "blog_url": "http://example.com/blog/",
    "clothing_size": "XS",
    "shoe_size": "40",
    "additional_comments": "Пример комментария",
    "status": "active",
    "ya_edu": 1,
    "amb_goals": [
        1
    ]
}

AMBASSADOR_RESP_EXAMPLE = AMBASSADOR_REQ_EXAMPLE | {
      "id": 1,
      "ya_edu": {
        "id": 1,
        "name": "Пример программы обучения"
      },
      "amb_goals": [
        {
          "id": 1,
          "name": "Пример цели"
        }
      ],
      "promo_code": "promo_code_example",
      "content_count": 0,
      "reg_date": f"{SCHEMA_DATE}T20:00:00.000+03:00",
      "country": 1,
      "city": 1
}
