import json
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Vendor, PurchaseOrder
from django.utils import timezone
from rest_framework.authtoken.models import Token


class VendorAPITestCase(APITestCase):
    def setUp(self):
        self.user, created = User.objects.get_or_create(
            username='testuser'
        )
        self.user.set_password('testpassword')
        self.user.save()

        self.token, created = Token.objects.get_or_create(user=self.user)
        self.vendor_data = {
            'name': 'Vendor Test',
            'contact_details': 'Test Contact Details',
            'address': 'Test Address',
            'vendor_code': 'VENDOR001',
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    def test_vendor_creation(self):
        self.authenticate()
        #  vendor code to ensure uniqueness
        unique_vendor_code = f'{self.vendor_data["vendor_code"]}_{timezone.now().timestamp()}'
        vendor_data_with_unique_code = {**self.vendor_data, 'vendor_code': unique_vendor_code}

        response = self.client.post('/api/vendors/', data=json.dumps(vendor_data_with_unique_code), content_type='application/json')
        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_vendor_update(self):
        self.authenticate()
        updated_data = {'name': 'Updated Vendor Name'}
        response = self.client.patch(f'/api/vendors/{self.vendor.pk}/', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        # Refresh vendor instance from the database
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_vendor_deletion(self):
        self.authenticate()
        response = self.client.delete(f'/api/vendors/{self.vendor.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(id=self.vendor.pk).exists())
    def test_purchase_order_creation(self):
        self.authenticate()
        purchase_order_data = {
            'po_number': f'PO_{timezone.now().timestamp()}',
            'vendor': self.vendor.pk,
            'order_date': timezone.now().isoformat(),
            'delivery_date': (timezone.now() + timezone.timedelta(days=7)).isoformat(),
            'items': {'item1': 'Product 1'},
            'quantity': 10,
            'status': 'pending',
            'issue_date': timezone.now().isoformat(),
        }
        response = self.client.post('/api/purchase_orders/', data=json.dumps(purchase_order_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('id' in response.data)
   
    def test_purchase_order_update(self):
        self.authenticate()
        # Create a PurchaseOrder instance with the Vendor instance
        purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor,  # Pass the Vendor instance directly
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=7),
            'items': {'item1': 'Product 1'},
            'quantity': 10,
            'status': 'pending',
            'issue_date': timezone.now(),
        }
        purchase_order = PurchaseOrder.objects.create(**purchase_order_data)

        # Print the purchase order data for debugging
        print(f"Purchase Order Data: {purchase_order_data}")

        updated_data = {'status': 'completed'}
        response = self.client.patch(
            f'/api/purchase_orders/{purchase_order.pk}/',  # Use PATCH instead of PUT for partial updates
            data=json.dumps(updated_data),
            content_type='application/json'
        )

        print(f"Response Content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh purchase_order instance from the database
        purchase_order.refresh_from_db()
        self.assertEqual(purchase_order.status, updated_data['status'])
    def test_purchase_order_deletion(self):
        self.authenticate()
        
        # Create a PurchaseOrder instance with the Vendor instance
        purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor,  # Pass the Vendor instance directly
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=7),
            'items': {'item1': 'Product 1'},
            'quantity': 10,
            'status': 'pending',
            'issue_date': timezone.now(),
        }
        purchase_order = PurchaseOrder.objects.create(**purchase_order_data)

        response = self.client.delete(f'/api/purchase_orders/{purchase_order.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PurchaseOrder.objects.filter(id=purchase_order.pk).exists())


    def test_vendor_performance(self):
        self.authenticate()
        response = self.client.get(f'/api/vendors/{self.vendor.pk}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('on_time_delivery_rate' in response.data)
        self.assertTrue('quality_rating_avg' in response.data)
        self.assertTrue('average_response_time' in response.data)
        self.assertTrue('fulfillment_rate' in response.data)
    def test_purchase_order_acknowledgment(self):
        self.authenticate()
        
        # Create a PurchaseOrder instance with the Vendor instance
        purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor,  # Pass the Vendor instance directly
            'order_date': timezone.now(),
            'delivery_date': timezone.now() + timezone.timedelta(days=7),
            'items': {'item1': 'Product 1'},
            'quantity': 10,
            'status': 'pending',
            'issue_date': timezone.now(),
        }
        purchase_order = PurchaseOrder.objects.create(**purchase_order_data)

        response = self.client.patch(f'/api/purchase_orders/{purchase_order.pk}/acknowledge/')
        print(f"Response Content: {response.content}")
        print(f"Response Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['acknowledgment_date'])
        
        # Refresh vendor instance from the database
        self.vendor.refresh_from_db()
        self.assertIsNotNone(self.vendor.average_response_time)
