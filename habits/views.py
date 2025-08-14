from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView

from habits.models import Habits
from habits.paginators import HabitListPagination
from habits.serliazers import HabitsSerializer

# Create your views here.


class HabitListView(ListAPIView):
    """
    Просмотор  привычки
    """

    serializer_class = HabitsSerializer
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habits.objects.filter(
            owner=self.request.user).order_by("action")


class PublicHabitListView(ListAPIView):
    """
    Просмотор всех привычки
    """

    serializer_class = HabitsSerializer

    def get_queryset(self):
        return Habits.objects.filter(publicity_flag=True).order_by("action")


class HabitCreateView(CreateAPIView):
    """
    создание  привычки
    """

    serializer_class = HabitsSerializer


class HabitUpdateView(UpdateAPIView):
    """
    Обновление привычки
    """

    serializer_class = HabitsSerializer

    def get_queryset(self):
        # Получаем привычки, принадлежащие текущему пользователю
        return Habits.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        # Сохраняем обновленную привычку
        serializer.save()

    def get_object(self):
        # Получаем привычку, которую нужно редактировать
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "У вас нет прав для изменения этой привычки.")
        return obj


class HabitDeleteView(DestroyAPIView):
    """
    Удаление  привычки
    """

    serializer_class = HabitsSerializer

    def get_queryset(self):
        # Получаем привычки, принадлежащие текущему пользователю
        return Habits.objects.filter(owner=self.request.user)

    def get_object(self):
        # Получаем привычку, которую нужно удалять
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "У вас нет прав для удаления этой привычки.")
        return obj
