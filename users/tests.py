from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class UserTests(APITestCase):
    def test_register_success(self):
        """Успешная регистрация пользователя."""
        url = reverse("register")
        data = {
            "email": "test@example.com",
            "password": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)

    def test_register_password_mismatch(self):
        """Неуспешная регистрация: пароли не совпадают."""
        url = reverse("register")
        data = {
            "email": "fail@example.com",
            "password": "123456",
            "password2": "654321",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_jwt_login(self):
        """Авторизация по JWT токену."""
        user = User.objects.create_user(
            email="login@example.com", password="testpass123"
        )
        url = reverse("token_obtain_pair")
        data = {"email": "login@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)