from multiprocessing.connection import Client

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_auth.app_settings import serializers
from rest_framework.reverse import reverse

user = get_user_model()

class UserCreateSerializersIsValidTests(TestCase):
    def setUp(self):
        self.validate_data = {
            'email': 'test0@gmail.com',
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test',
            're_password': 'test'
        }
        self.not_valid_data = self.validate_data.copy()
        self.not_valid_data['email'] = 'test@gmail'
        self.not_valid_data['password'] = 'test2'

    def test_user_serializers_is_valid(self):
        serializers = UserCreateSerializer(data=self.validate_data)
        self.assertTrue(serializers.is_valid())
        self.assertEqual(serializers.errors, {})

    def test_user_create_password_mismatch(self):
        data = {
            "email": "test2@example.com",
            "username": "testuser2",
            "first_name": "Test2",
            "last_name": "User2",
            "password": "password1",
            "re_password": "password2"
        }
    def test_user_create_serializers(self):
        serializers = UserCreateSerializers(data=self.validate_data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        self.assertEqual(user.email, 'test0@gmail.com')
        self.assertEqual(user.first_name, 'test')
        self.assertTrue(user.check_password('test'))

    def test_user_serializer_not_valid(self):
        serializers = UserCreateSerializers(data=self.not_valid_data)
        self.assertFalse(serializers.is_valid())
        self.assertEqual(serializers.errors, {'email': ['test@gmail.'],'password':['test2.']})

    def test_user_serializer_not_valid_email(self):
        serializers = UserCreateSerializers(data=self.not_valid_data)
        self.assertFalse(serializers.is_valid())
        self.assertEqual(serializers.errors, {'email': ['test@gmail.'],'password':['test2.']})



class UserRegisterSerializersTests(TestCase):
    def setUp(self):
        self.register_data = {
            'email': 'test0@gmail.com',
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test',
            're_password': 'test'
        }
        self.client = Client()
        self.register_url = reverse('register')

    def test_user_register_serializers(self):
        response = self.client.post(
            self.register_url,
            data=self.register_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test')




