from ambassadors.factories import AmbassadorFactory, PromoCodeFactory
from ambassadors.models import PromoCode
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class PromoCodeViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        """
        Фикстура для тестов промокодов.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        cls.ambassador = AmbassadorFactory()
        cls.promo_code = PromoCodeFactory(status='active')
        cls.url = reverse('promocode-list')
        cls.detail_url = reverse(
            'promocode-detail', args=(cls.promo_code.id,)
        )

    def setUp(self):
        """
        Фикстура для каждого теста промокодов.
        """
        self.client.force_authenticate(user=self.user)

    def test_get_all_promo_codes(self):
        """
        Тест на получение списка всех промокодов.
        """
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_only_one_active_promo_code(self):
        PromoCode.objects.create(
            name='active_promo_code',
            status='active',
            ambassador=self.promo_code.ambassador
        )
        with self.assertNumQueries(1):
            response = self.client.get(self.url)
        active_count = sum(
            1 for data in response.data if data['status'] == 'active'
        )
        self.assertEqual(active_count, 1)

    def test_get_single_promo_code(self):
        """
        Тест на получение одного промокода.
        """
        with self.assertNumQueries(1):
            response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.promo_code.id)

    def test_create_promo_code(self):
        """
        Тест на создание нового промокода.
        """
        new_promo_code_data = {
            'name': 'test_promo_code',
            'status': 'active',
            'ambassador': self.ambassador.pk
        }
        response = self.client.post(self.url, new_promo_code_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], new_promo_code_data['name'])

    def test_update_promo_code(self):
        """
        Тест на обновление промокода.
        """
        updated_data = {'name': 'new_promo_code'}
        response = self.client.patch(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_promo_code(self):
        """
        Тест на удаление промокода.
        """
        promo_code = PromoCodeFactory()
        detail_url = reverse('promocode-detail', args=(promo_code.id,))
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PromoCode.objects.filter(id=promo_code.id).exists())
