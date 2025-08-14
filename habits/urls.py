from django.urls import path

from habits.apps import AtomicHabitsConfig
from habits.views import HabitCreateView, HabitDeleteView, HabitListView, HabitUpdateView, PublicHabitListView

# Описание маршрутизации для User

app_name = AtomicHabitsConfig.name

urlpatterns = [
    path("habits_list/", HabitListView.as_view(), name="habits_list"),
    path(
        "habits_public_list/",
        PublicHabitListView.as_view(),
        name="habits_public_list"),
    path("habits_create/", HabitCreateView.as_view(), name="habits_create"),
    path(
        "habits_update/<int:pk>/",
        HabitUpdateView.as_view(),
        name="habits_update"),
    path(
        "habits_delete/<int:pk>/",
        HabitDeleteView.as_view(),
        name="habits_delete"),
]
