from ambassadors.factories import (
    AmbassadorFactory,
    AmbassadorGoalFactory,
    CityFactory,
    CountryFactory,
    TrainingProgramFactory,
    ContentFactory
)
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
        with self.assertNumQueries(5):
            response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_single_ambassador(self):
        """
        Тест на получение данных одного амбассадора.
        """
        with self.assertNumQueries(4):
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


class AmbassadorFilterTestCase(APITestCase):
    """
    Класс для тестирования фильтров амбассадоров.
    """

    def setUp(self):
        """
        Настройка начальных условий для тестов.
        """
        self.list_url = reverse('ambassador-list')
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.program1 = TrainingProgramFactory()
        self.program2 = TrainingProgramFactory()
        self.country1 = CountryFactory()
        self.country2 = CountryFactory()
        self.city1 = CityFactory()
        self.city2 = CityFactory()
        self.ambassador1 = AmbassadorFactory(
            ya_edu=self.program1, country=self.country1,
            city=self.city1, status='active', gender='М'
        )
        self.ambassador2 = AmbassadorFactory(
            ya_edu=self.program2, country=self.country2,
            city=self.city2, status='inactive', gender='Ж'
        )
        self.content = ContentFactory(ambassador=self.ambassador1)
        self.client.force_authenticate(user=self.user)

    def test_filter_by_ya_edu(self):
        """
        Тест фильтра по программе обучения амбассадора.
        """
        response = self.client.get(self.list_url, {'ya_edu': self.program1.id})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)

    def test_filter_by_country(self):
        """
        Тест фильтра по стране амбассадора.
        """
        response = self.client.get(self.list_url, {'country': self.country1.id})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)

    def test_filter_by_city(self):
        """
        Тест фильтра по городу амбассадора.
        """
        response = self.client.get(self.list_url, {'city': self.city1.id})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)

    def test_filter_by_status(self):
        """
        Тест фильтра по статусу амбассадора.
        """
        response = self.client.get(self.list_url, {'status': 'active'})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)

    def test_filter_by_gender(self):
        """
        Тест фильтра по полу амбассадора.
        """
        response = self.client.get(self.list_url, {'gender': 'М'})
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)

    def test_ordering_by_reg_date(self):
        """
        Тест сортировки по дате регистрации амбассадора.
        """
        response = self.client.get(self.list_url, {'order': 'date'})
        self.assertEqual(response.data['results'][0]['id'],
                         self.ambassador1.id)
        self.assertEqual(response.data['results'][1]['id'],
                         self.ambassador2.id)

    def test_ordering_by_full_name(self):
        """
        Тест сортировки по имени амбассадора.
        """
        response = self.client.get(self.list_url, {'order': 'name'})
        names = [amb['full_name'] for amb in response.data['results']]
        self.assertEqual(names, sorted(names))

    def test_ordering_by_content(self):
        """
        Тест сортировки по кол-ву контента амбассадора.
        """
        response = self.client.get(self.list_url, {'order': '-content'})
        self.assertEqual(response.data['results'][0]['content_count'], 1)
