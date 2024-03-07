from ambassadors.factories import (AmbassadorFactory, AmbassadorGoalFactory,
                                   CityFactory, CountryFactory,
                                   TrainingProgramFactory)
from ambassadors.models import Ambassador
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AmbassadorViewSetTestCase(APITestCase):
    """
    Класс для тестирования амбассадоров.
    """

    def setUp(self):
        """
        Настройка начальных условий для тестов.
        """
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.training_program = TrainingProgramFactory()
        self.ambassador_goal = AmbassadorGoalFactory()
        self.country = CountryFactory()
        self.city = CityFactory()
        self.ambassador = AmbassadorFactory()
        self.list_url = reverse('ambassador-list')
        self.detail_url = reverse('ambassador-detail',
                                  kwargs={'pk': self.ambassador.pk})
        self.client.force_authenticate(user=self.user)

    def test_get_all_ambassadors(self):
        """
        Тест на получение списка всех амбассадоров.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_single_ambassador(self):
        """
        Тест на получение данных одного амбассадора.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], self.ambassador.full_name)

    def test_create_ambassador(self):
        """
        Тест на создание нового амбассадора.
        """
        new_ambassador_data = {
            'full_name': 'Новый Амбассадор',
            'gender': 'Ж',
            'ya_edu': self.training_program.id,
            'amb_goals': [self.ambassador_goal.id],
            'country': 'Турция',
            'city': 'Стамбул',
            'address': 'Новый адрес',
            'postal_code': '123123',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'telegram': '@newambassador',
            'edu': 'Новое образование',
            'work': 'Новое место работы',
            'study_goal': 'Новая цель обучения',
            'clothing_size': 'L',
            'shoe_size': '44'
        }
        response = self.client.post(self.list_url, new_ambassador_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'Новый Амбассадор')

    def test_update_ambassador(self):
        """
        Тест на обновление данных амбассадора.
        """
        updated_data = {'full_name': 'Обновленный Амбассадор'}
        response = self.client.patch(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Обновленный Амбассадор')

    def test_delete_ambassador(self):
        """
        Тест на удаление амбассадора.
        """
        ambassador = AmbassadorFactory()
        detail_url = reverse('ambassador-detail', kwargs={'pk': ambassador.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ambassador.objects.filter(pk=ambassador.pk).exists())
