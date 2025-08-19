from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer, HabitPublicSerializer


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Показываем только привычки текущего пользователя"""
        return Habit.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        """При создании привычки автоматически привязываем к текущему пользователю"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public", permission_classes=[])
    def public_habits(self, request):
        """Список публичных привычек всех пользователей, доступен без авторизации"""
        public_habits = Habit.objects.filter(is_public=True).order_by("-created_at")
        serializer = HabitPublicSerializer(public_habits, many=True)
        return Response(serializer.data)
