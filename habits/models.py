from django.db import models
from rest_framework.exceptions import ValidationError

from config import settings

# Create your models here.


class Habits(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )
    place = models.CharField(
        max_length=250,
        verbose_name="Место выполнения",
        help_text="Введите Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    pleasant_habit_flag = models.BooleanField(
        max_length=250, verbose_name="Признак приятной привычки", help_text="Введите Признак"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"pleasant_habit_flag": True},
        verbose_name="Связанная привычка",
    )  # ForeignKey self
    frequency = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Вознаграждение ", help_text="Введите Вознаграждение "
    )
    time_to_perform = models.PositiveIntegerField(
        verbose_name="Время на выполнение")  # Int+
    publicity_flag = models.BooleanField(
        default=False, verbose_name="Признак публичности")

    def __str__(self):
        return self.action

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя совмещать вознаграждение и связанную привычку.")
        if self.time_to_perform > 120:
            raise ValidationError(
                "Время выполнения не должно быть больше 120 минут.")
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError(
                "Периодичность выполнения должна быть от 1 до 7 дней")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("remove_any_product", "Remove any product"),
        # ]
