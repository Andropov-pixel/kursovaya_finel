from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from habit.models import Habit


class HabitTests(APITestCase):
    def setUp(self):
        """Создаем пользователя и авторизуем его."""
        self.user = User.objects.create_user(
            email="user1@example.com", password="12345"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест создания привычки."""
        url = reverse("habit-list")
        data = {
            "place": "дом",
            "time": "10:00",
            "action": "читать",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 60,
            "is_public": True,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)

        habit = Habit.objects.first()
        self.assertEqual(habit.user, self.user)

    def test_list_user_habits(self):
        """Тест получения списка привычек текущего пользователя."""
        Habit.objects.create(
            user=self.user,
            place="дом",
            time="10:00",
            action="читать",
            execution_time=30,
        )
        url = reverse("habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_public_habits(self):
        """Тест получения публичных привычек."""
        user2 = User.objects.create_user(email="user2@example.com", password="pass")
        Habit.objects.create(
            user=user2,
            place="офис",
            time="09:00",
            action="пить воду",
            is_public=True,
            execution_time=60,
        )
        url = reverse("habit-public-habits")
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
