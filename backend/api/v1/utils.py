import io

import openpyxl
from rest_framework import renderers

HEADER = ['name_merch', 'ambassador', 'status_send', 'created_date', 'comment']


def format_telegram_username(input_str: str) -> str:
    """
    Функция принимает строку и преобразует ее в формат '@username'.
    """
    if input_str.startswith('https://t.me/'):
        username = '@' + input_str.split('/')[-1]
    else:
        username = input_str if input_str.startswith('@') else f'@{input_str}'
    return username


class ExcelRender(renderers.BaseRenderer):
    """
    Класс преобразует данные в формат excel
    """
    media_type = "aapplication/vnd.ms-excel"
    format = "xls"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        workbook = openpyxl.Workbook()
        buffer = io.BytesIO()
        ws = workbook.active
        ws.append(HEADER)

        for merch_data in data:
            ws.append(list(merch_data.values()))

        workbook.save(buffer)
        return buffer.getvalue