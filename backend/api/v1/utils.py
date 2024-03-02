def format_telegram_username(input_str: str) -> str:
    """
    Функция принимает строку и преобразует ее в формат '@username'.
    """
    if input_str.startswith('https://t.me/'):
        username = '@' + input_str.split('/')[-1]
    else:
        username = input_str if input_str.startswith('@') else f'@{input_str}'
    return username
