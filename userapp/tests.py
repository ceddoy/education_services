from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from userapp.models import User


class TestUserAuthorisation(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(email='mail01@mail.ru', password='123454321qw')
        cls.api_auth_token_url = reverse("get_token")

    def test_get_token_auth_invalid(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': '335rtdsfg335'
        }
        response = self.client.post(self.api_auth_token_url, data)
        self.assertTrue(isinstance(response.data.get('non_field_errors')[0], ErrorDetail))
        self.assertTrue('authorization' == response.data.get('non_field_errors')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token_auth_email_invalid(self):
        data = {
            'email': 'mail01',
            'password': '335rtdsfg335'
        }
        response = self.client.post(self.api_auth_token_url, data)
        self.assertTrue(isinstance(response.data.get('email')[0], ErrorDetail))
        self.assertTrue('invalid' == response.data.get('email')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token_auth_valid(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': '123454321qw'
        }
        response = self.client.post(self.api_auth_token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


class TestUserCreate(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_create_user_url = reverse("create_user")

    def test_create_user_valid(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': '123454321qw'
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_email(self):
        data = {
            'email': 'mail01',
            'password': '123454321qw'
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertTrue('email' in response.data.keys())
        self.assertTrue(isinstance(response.data.get('email')[0], ErrorDetail))
        self.assertTrue('invalid' == response.data.get('email')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_field_email(self):
        data = {
            'email': '',
            'password': '123454321qw'
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertTrue('email' in response.data.keys())
        self.assertTrue(isinstance(response.data.get('email')[0], ErrorDetail))
        self.assertTrue('blank' == response.data.get('email')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_already_exists_email(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': '123454321qw'
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.api_create_user_url, data)
        self.assertTrue('email' in response.data.keys())
        self.assertTrue(isinstance(response.data.get('email')[0], ErrorDetail))
        self.assertTrue('unique' == response.data.get('email')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_invalid_password(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': '123'
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertTrue('password' in response.data.keys())
        self.assertTrue(isinstance(response.data.get('password')[0], ErrorDetail))
        self.assertTrue('password_too_short' == response.data.get('password')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_empty_field_password(self):
        data = {
            'email': 'mail01@mail.ru',
            'password': ''
        }
        response = self.client.post(self.api_create_user_url, data)
        self.assertTrue('password' in response.data.keys())
        self.assertTrue(isinstance(response.data.get('password')[0], ErrorDetail))
        self.assertTrue('blank' == response.data.get('password')[0].code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # def test_view_list_logs_with_token(self):
    #     auth = self.client.post('/api-token-auth/', {'email': 'mail01@mail.ru', 'password': '123454321qw'})
    #     token = f'Token {auth.data.get("token")}'
    #     self.client.credentials(HTTP_AUTHORIZATION=token)
    #     response = self.client.get('/api/logs/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data.get('count'), User.objects.all().count())
