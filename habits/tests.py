from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habits

# Create your tests here.

User = get_user_model()


class HabitsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345")

    def test_creating_habit(self):
        habit = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=True,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            publicity_flag=True,
            owner=self.user,
        )
        self.assertIsInstance(habit, Habits)
        self.assertEqual(habit.action, "Действие")
        self.assertEqual(habit.place, "место")
        self.assertEqual(habit.frequency, 2)

    def test_habit_string_representation(self):
        habits = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=True,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            publicity_flag=True,
            owner=self.user,
        )
        self.assertEqual(str(habits), habits.action)


class HabitsSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="12345")
        self.valid_habit_data = {
            "place": "Дом",
            "time": "8:00:00",
            "action": "зарядка",
            "pleasant_habit_flag": True,
            "frequency": 3,
            "reward": None,
            "time_to_complete": 120,
            "publicity_flag": True,
        }

    def test_invalid_habit_with_both_reward_and_related_habit(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["reward"] = "Какое-то вознаграждение"
        invalid_data["related_habit"] = True

    def test_invalid_time_to_complete(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["time_to_complete"] = 121  # Пример недопустимого значения

    def test_invalid_frequency(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["frequency"] = 8  # Пример недопустимого значения


class HabitAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", password="12345")
        self.client.force_authenticate(user=self.user)

        self.habits = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=False,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            publicity_flag=False,
            owner=self.user,
        )

    def test_create_habit(self):
        response = self.client.post(
            "/habits/habits_create/",
            {
                "place": "место",
                "time": "14:00:00",
                "action": "Действие",
                "pleasant_habit_flag": False,
                "frequency": 2,
                "reward": "Вознаграждение",
                "time_to_perform": 100,
                "publicity_flag": False,
                "owner": 100,
            },

        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Действие")

    def test_update_habit(self):
        response = self.client.patch(
            f"/habits/habits_update/{self.habits.id}/",
            {"action": "Другое действие", "frequency": 5},

        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habits.refresh_from_db()
        self.assertEqual(self.habits.action, "Другое действие")
        self.assertEqual(self.habits.frequency, 5)

    def test_delete_habit(self):
        response = self.client.delete(f"/habits/habits_delete/{self.habits.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.filter(id=self.habits.id).exists())

    def test_list_user_habits(self):
        response = self.client.get("/habits/habits_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_public_habits(self):
        public_habit = Habits.objects.create(
            owner=self.user,
            place="дом",
            time="07:00:00",
            action="зарядка",
            pleasant_habit_flag=True,
            frequency=1,
            reward=None,
            time_to_perform=120,
            publicity_flag=True,
        )
        response = self.client.get("/habits/habits_public_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(public_habit.action, [habits["action"] for habits in response.data])