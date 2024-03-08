from django.urls import reverse
from rest_framework import status

from ambassadors.factories import AmbassadorFactory, ContentFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class ContentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.ambassador = AmbassadorFactory(telegram='@testuser')
        self.content = ContentFactory()
        self.list_url = reverse('content-list')
        self.detail_url = reverse(
            'content-detail', kwargs={'pk': self.content.pk}
        )
        self.client.force_authenticate(user=self.user)

    def test_get_all_content(self):
        self.content2 = ContentFactory()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_content(self):
        new_content_data = {
            'full_name': self.ambassador.full_name,
            'telegram': self.ambassador.telegram,
            'link': 'https://www.content.com',
            'guide': 'Да',
        }
        response = self.client.post(self.list_url, new_content_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], self.ambassador.full_name)
        self.assertEqual(response.data['ambassador'], self.ambassador.pk)
        self.assertEqual(response.data['link'], new_content_data['link'])
        self.assertEqual(response.data['guide'], True)
        self.assertEqual(response.data['status'], 'new')

    def test_create_content_with_unexpected_telegram(self):
        new_content_data = {
            'full_name': self.ambassador.full_name,
            'telegram': '@wrongtestuser',
            'link': 'https://www.content.com',
            'guide': '',
        }
        response = self.client.post(self.list_url, new_content_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], self.ambassador.full_name)
        self.assertEqual(response.data['ambassador'], None)
        self.assertEqual(response.data['link'], new_content_data['link'])
        self.assertEqual(response.data['guide'], False)
        self.assertEqual(response.data['status'], 'new')

    def test_update_content_status(self):
        new_status_request = {'status': 'rejected'}
        response = self.client.patch(self.detail_url, new_status_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], new_status_request['status'])
