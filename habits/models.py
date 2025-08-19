from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",  # Связь с пользователем (user.habits)
    )
    place = models.CharField(max_length=255)  # Место выполнения привычки
    time = models.TimeField()  # Время выполнения
    action = models.CharField(max_length=255)  # Действие (сама привычка)
    is_pleasant = models.BooleanField(default=False)  # Приятная привычка?
    is_public = models.BooleanField(default=True)  # Видна другим пользователям?
    periodicity = models.PositiveIntegerField(default=1)  # Раз в сколько дней
    execution_time = models.PositiveIntegerField()  # Время выполнения в секундах
    reward = models.CharField(max_length=255, blank=True)  # Вознаграждение
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",  # Обратная связь, если нужно
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления

    def clean(self):
        # Только одно из двух: награда или связанная привычка
        if self.reward and self.related_habit:
            raise ValidationError(
                _("Нельзя указывать и награду, и связанную привычку одновременно.")
            )

        # Приятная привычка не может иметь награду или связь
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                _("Приятная привычка не может иметь награду или связанную привычку.")
            )

        # Только приятные привычки могут быть связаны
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(_("Связана может быть только приятная привычка."))

        # Время выполнения ≤ 120 сек
        if self.execution_time > 120:
            raise ValidationError(_("Время выполнения не должно превышать 120 секунд."))

        # Периодичность от 1 до 7
        if not (1 <= self.periodicity <= 7):
            raise ValidationError(_("Периодичность должна быть от 1 до 7 дней."))

    def __str__(self):
        return f"{self.action} в {self.time.strftime('%H:%M')} ({self.user.email})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]