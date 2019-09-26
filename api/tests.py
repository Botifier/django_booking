from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Property, Booking

    
class PropertyBookingsViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'pass1234')
        self.property = Property.objects.create(property_name='pname', property_id='pid', city='pcity')
        self.booking1 = Booking.objects.create(property = self.property, user = self.user)
        self.booking2 = Booking.objects.create(property = self.property, user = self.user)

    def test_get_bookings(self):
        url = reverse('properties_bookings-list', kwargs={'property_id':self.property.property_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], str(self.booking1.uuid))
        self.assertEqual(response.data[1]['id'], str(self.booking2.uuid))

    def test_invalid_property_id(self):
        url = reverse('properties_bookings-list', kwargs={'property_id':404})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserBookingsViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', 'pass1234')
        self.property = Property.objects.create(property_name='pname', property_id='pid', city='pcity')
        self.booking1 = Booking.objects.create(property = self.property, user = self.user)
        self.booking2 = Booking.objects.create(property = self.property, user = self.user)

    def test_get_user_bookings(self):
        url = reverse('users_bookings-list', kwargs={'user_id':self.user.uuid})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], str(self.booking1.uuid))
        self.assertEqual(response.data[1]['id'], str(self.booking2.uuid))

    def test_invalid_user_id(self):
        url = reverse('users_bookings-list', kwargs={'user_id':'deadbeef-cafe-cafe-cafe-deadbeefbabe'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BookingCreateViewTest(APITestCase):
    API_URL = reverse('booking')

    def setUp(self):
        auth_url = reverse('register')
        # self.user = User.objects.create_user('testuser', 'pass1234')
        response = self.client.post(
            auth_url, 
            {'username':'testuser', 'password':'pass1234'},
             format='json'
        )
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])
        self.user_id = response.data['user_id']

    def test_create_booking_existing_property(self):
        property = Property.objects.create(property_name='pname', property_id='pid', city='pcity')
        booking_data = {
            'property': {
                'property_id': property.property_id,
                'property_name': property.property_name,
                'city': property.city,
            }
        }
        response = self.client.post(self.API_URL, booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        stored_booking = Booking.objects.get()
        self.assertEqual(stored_booking.user.uuid, self.user_id)
        self.assertEqual(stored_booking.property.property_id, booking_data['property']['property_id'])
        self.assertEqual(stored_booking.property.property_name, booking_data['property']['property_name'])
        self.assertEqual(stored_booking.property.city, booking_data['property']['city'])

    def test_create_booking_normal(self):
        booking_data = {
            'property': {
                'property_id': 'test_id',
                'property_name': 'test_name',
                'city': 'test_city',
            }
        }
        response = self.client.post(self.API_URL, booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        stored_property = Property.objects.get()
        self.assertEqual(stored_property.property_id, 'test_id')
        self.assertEqual(stored_property.property_name, 'test_name')
        self.assertEqual(stored_property.city, 'test_city')

        stored_booking = Booking.objects.get()
        self.assertEqual(stored_booking.user.uuid, self.user_id)
        self.assertEqual(stored_booking.property.property_id, booking_data['property']['property_id'])
        self.assertEqual(stored_booking.property.property_name, booking_data['property']['property_name'])
        self.assertEqual(stored_booking.property.city, booking_data['property']['city'])

    def test_create_unvalid_booking(self):
        booking_data = {}
        response = self.client.post(self.API_URL, booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)