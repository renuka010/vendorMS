from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder, Performance
from django.utils import timezone
from datetime import timedelta


class VendorViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='Test Code',
        )

    def test_list_vendors(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor.name)
        self.assertEqual(
            response.data[0]['contact_details'], self.vendor.contact_details)
        self.assertEqual(response.data[0]['address'], self.vendor.address)
        self.assertEqual(
            response.data[0]['vendor_code'], self.vendor.vendor_code)

    def test_retrieve_vendor(self):
        response = self.client.get(
            reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)
        self.assertEqual(
            response.data['contact_details'], self.vendor.contact_details)
        self.assertEqual(response.data['address'], self.vendor.address)
        self.assertEqual(response.data['vendor_code'], self.vendor.vendor_code)

    def test_retrieve_vendor_not_found(self):
        non_existent_id = 123456
        response = self.client.get(
            reverse('vendor-detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vendor(self):
        data = {
            'name': 'New Vendor',
            'contact_details': 'New Contact Details',
            'address': 'New Address',
            'vendor_code': 'New Code',
        }
        response = self.client.post(reverse('vendor-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_update_vendor(self):
        data = {
            'name': 'Updated Vendor',
        }
        response = self.client.patch(
            reverse('vendor-detail', kwargs={'pk': self.vendor.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, data['name'])

    def test_delete_vendor(self):
        response = self.client.delete(
            reverse('vendor-detail', kwargs={'pk': self.vendor.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_delete_vendor_not_found(self):
        non_existent_id = 123456
        response = self.client.delete(
            reverse('vendor-detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PurchaseOrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='Test Code',
        )

        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=10),
            items={'item1': 'my item1'},
            quantity=15,
            status='pending',
            issue_date=timezone.now(),
        )

    def test_list_purchase_orders(self):
        response = self.client.get(reverse('purchaseorder-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['po_number'], self.purchase_order.po_number)
        self.assertEqual(response.data[0]['items'], self.purchase_order.items)

    def test_create_purchase_order(self):
        data = {
            'po_number': 'PO456',
            'vendor': self.vendor.id,
            'order_date': timezone.now() - timedelta(days=2),
            'delivery_date': timezone.now() + timedelta(days=1),
            'items': {'item1': 'my item2'},
            'quantity': 100,
            'status': 'pending',
            'issue_date': timezone.now() - timedelta(days=2),
        }
        response = self.client.post(
            reverse('purchaseorder-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)
        self.assertEqual(PurchaseOrder.objects.get(
            po_number='PO456').quantity, 100)

    def test_retrieve_purchase_order(self):
        response = self.client.get(
            reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'],
                         self.purchase_order.po_number)
        self.assertEqual(response.data['quantity'],
                         self.purchase_order.quantity)

    def test_retrieve_purchase_order_not_found(self):
        non_existent_id = 123456
        response = self.client.get(
            reverse('purchaseorder-detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchase_order(self):
        data = {
            'quantity': 200,
        }
        response = self.client.patch(
            reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.quantity, data['quantity'])

    def test_delete_purchase_order(self):
        response = self.client.delete(
            reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_delete_purchase_order_not_found(self):
        non_existent_id = 123456
        response = self.client.delete(
            reverse('purchaseorder-detail', kwargs={'pk': non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_acknowledge_purchase_order(self):
        response = self.client.post(
            reverse('purchaseorder-acknowledge', kwargs={'pk': self.purchase_order.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)


class PerformanceViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact Details',
            address='Test Address',
            vendor_code='Test Code',
        )

        self.performance = Performance.objects.create(
            vendor=self.vendor,
            on_time_delivery_rate=0.9,
            quality_rating_avg=4.5,
            average_response_time=2.0,
            fulfillment_rate=0.95,
        )

    def test_retrieve_vendor_performance(self):
        response = self.client.get(
            reverse('vendor_performance', kwargs={'vendor_id': self.vendor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]['on_time_delivery_rate'], self.performance.on_time_delivery_rate)
        self.assertEqual(
            response.data[0]['quality_rating_avg'], self.performance.quality_rating_avg)
        self.assertEqual(
            response.data[0]['average_response_time'], self.performance.average_response_time)
        self.assertEqual(
            response.data[0]['fulfillment_rate'], self.performance.fulfillment_rate)

    def test_retrieve_vendor_performance_not_found(self):
        non_existent_id = 123456
        response = self.client.get(
            reverse('vendor_performance', kwargs={'vendor_id': non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
