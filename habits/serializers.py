from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для модели Habit,
    используемый для создания, редактирования и чтения привычек.
    """

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        """
        Валидация данных, дублирующая логику модели.
        """
        reward = data.get("reward", "")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant", False)
        execution_time = data.get("execution_time", 0)
        periodicity = data.get("periodicity", 1)

        # Проверка: нельзя одновременно указывать вознаграждение и связанную привычку
        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя указывать и награду, и связанную привычку одновременно."
            )

        # Приятная привычка не может иметь награду или связанную привычку
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "Приятная привычка не может иметь награду или связанную привычку."
            )

        # Связанная привычка должна быть именно приятной
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанной может быть только приятная привычка."
            )

        # Время выполнения не больше 120 секунд
        if execution_time > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд."
            )

        # Периодичность в пределах от 1 до 7 дней
        if not (1 <= periodicity <= 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        return data


class HabitPublicSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичных привычек.
    """

    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "execution_time",
        )
        read_only_fields = fields
