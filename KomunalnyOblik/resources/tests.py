from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import Resource, CustomUser
from .views import GetDataView, CreateView, UpdateDeleteView
from .serializers import ResourcesSerializer
from rest_framework.authtoken.models import Token
from .auth_view import TokenAuthView, RegisterUserView


class GetDataViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_data_view(self):
        resource_1 = Resource.objects.create(
            resource_name='Resource_1',
            unit_price=10.0,
            consumed_per_month=20.0,
            expenses_per_month=200.0,
            month='January',
        )

        resource_2 = Resource.objects.create(
            resource_name='Resource_2',
            unit_price=15.0,
            consumed_per_month=25.0,
            expenses_per_month=250.0,
            month='February',
        )

        url = '/api-accountant/'
        request = self.factory.get(url)
        response = GetDataView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = ResourcesSerializer([resource_1, resource_2], many=True).data
        self.assertEqual(response.data, expected_data)

class CreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
    def test_create_resource(self):
        view = CreateView.as_view()
        url = '/api-worker/'
        data = {
            'resource_name': 'Test Resource',
            'unit_price': 10.0,
            'consumed_per_month': 20.0,
            'expenses_per_month': 200.0,
            'month': 'January',
        }
        request = self.factory.post(url, data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 1)



class UpdateDeleteViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.resource = Resource.objects.create(
            resource_name='Test_Resource',
            unit_price=10.0,
            consumed_per_month=20.0,
            expenses_per_month=200.0,
            month='Test_month',
        )

    def test_delete_resource(self):
        url = f'/api-worker/<int:pk>/{self.resource.pk}/'

        request = self.factory.delete(url)
        response = UpdateDeleteView.as_view()(request, pk=self.resource.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Resource.objects.filter(pk=self.resource.pk).exists())

    def test_update_resource(self):
        url = f'/api-worker/<int:pk>/{self.resource.pk}/'

        data = {
            'resource_name': 'Updated_Resource',
            'unit_price': 15.152,
            'consumed_per_month': 567.0,
            'expenses_per_month': 0,
            'month': 'February',
        }

        request = self.factory.put(url, data, format='json')
        response = UpdateDeleteView.as_view()(request, pk=self.resource.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_resource = Resource.objects.get(pk=self.resource.pk)
        self.assertEqual(updated_resource.resource_name, 'Updated_Resource')
        self.assertEqual(updated_resource.unit_price, 15.152)
        self.assertEqual(updated_resource.consumed_per_month, 567.0)
        self.assertEqual(updated_resource.expenses_per_month, 0)
        self.assertEqual(updated_resource.month, 'February')

class TokenAuthViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = '/token-auth/'
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )
    def test_token_auth_view(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        request = self.factory.post(self.url, data, format='json')
        response = TokenAuthView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('email', response.data)
        user_token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], user_token.key)

    def test_token_auth_view_failure(self):
        data = {'username': 'wrongtestuser', 'password': 'wrongtestpassword'}
        request = self.factory.post(self.url, data, format='json')
        response = TokenAuthView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RegistrationAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RegisterUserView.as_view()
        self.url = '/register/'
    def test_user_registration_success(self):
        data = {'username': 'happy', 'password': '12345'}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='happy').exists())
    def test_user_registration_failure(self):
        existing_user = CustomUser.objects.create_user(username='happy', password='12345')
        data = {'username': 'happy', 'password': '12345'}
        request = self.factory.post(self.url, data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CustomUser.objects.filter(username='newuser').exists())

