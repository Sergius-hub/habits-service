from django.db import models
from datetime import time as dt_time
from datetime import timedelta

from django.conf import settings

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True

class Habit(TimeStampModel):
    """Модель привычки"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь"
    )

    place = models.CharField(
        max_length=100,
        verbose_name="Место"
    )

    time = models.TimeField(
        default=dt_time( 9, 0 ),
        verbose_name="Время выполнения"
    )

    action = models.CharField(
        max_length=100,
        verbose_name="Действие"
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки"
    )

    associated_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_habits",
        verbose_name="Связанная привычка"
    )

    period = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)"
    )

    reward = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Вознаграждение"
    )

    time_to_action = models.DurationField(
        default=timedelta( seconds=60 ),
        verbose_name="Время на выполнение"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Признак публикации"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} в {self.time}"