from ambassadors.factories import (
    AmbassadorFactory,
    MerchandiseFactory,
    MerchandiseShippingRequestFactory,
)
from ambassadors.models import MerchandiseShippingRequest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class MerchandiseShippingRequestTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.ambassador = AmbassadorFactory()
        self.merch = MerchandiseFactory()
        self.shipping_request = MerchandiseShippingRequestFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_shipping_requests_list(self):
        url = '/api/v1/merchandise/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_merch(self):
        url = '/api/v1/merchandise/'
        new_merchandise_data = {
            'status_send': "new",
            'comment': "Комментарий",
            'name_merch': self.merch.pk,
            'ambassador': self.ambassador.pk
        }
        response = self.client.post(url, new_merchandise_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status_send'], new_merchandise_data['status_send'])

    def test_update_merch(self):
        merchandise = MerchandiseShippingRequest.objects.create(
            status_send="new",
            comment="Комментарий",
            name_merch=self.merch,
            ambassador=self.ambassador)
        url = f'/api/v1/merchandise/{merchandise.pk}/'
        updated_merchandise_data = {
            'status_send': "address_verified",
            'comment': "Обновленный комментарий",
            'name_merch': self.merch.pk,
            'ambassador': self.ambassador.pk
        }
        response = self.client.patch(url, updated_merchandise_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_merchandise = MerchandiseShippingRequest.objects.get(pk=merchandise.pk)
        self.assertEqual(updated_merchandise.status_send, updated_merchandise_data['status_send'])
        self.assertEqual(updated_merchandise.comment, updated_merchandise_data['comment'])
