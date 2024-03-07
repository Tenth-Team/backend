from api.v1.utils import format_telegram_username
from django.test import TestCase


class FormatTelegramUsernameTest(TestCase):
    """
    Класс для тестирования функции, которая преобразует username телеграма.
    """

    def test_format_username_with_at_sign(self):
        """
        Тест проверяет, что username начинающийся с @ не изменяется.
        """
        username = '@username'
        formatted_username = format_telegram_username(username)
        self.assertEqual(formatted_username, '@username')

    def test_format_username_without_at_sign(self):
        """
        Тест проверяет, что к username добавляется @, если он отсутствует.
        """
        username = 'username'
        formatted_username = format_telegram_username(username)
        self.assertEqual(formatted_username, '@username')

    def test_format_username_from_telegram_link(self):
        """
        Тест проверяет, что из ссылки Telegram извлекается username.
        """
        username = 'https://t.me/username'
        formatted_username = format_telegram_username(username)
        self.assertEqual(formatted_username, '@username')
