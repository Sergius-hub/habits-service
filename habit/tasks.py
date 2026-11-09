import json
import logging
from datetime import datetime

import requests
from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habit.models import Habit
from config.settings import TG_API_KEY

logger = logging.getLogger(__name__)

@shared_task
def create_periodic_tasks():
    habits = Habit.objects.all()

    for habit in habits:
        if not habit.user.chat_id:
            logger.warning( "Habit %s: у пользователя нет chat_id, пропускаем", habit.pk )
            continue
        if not PeriodicTask.objects.filter(name=f"Send message {habit.user.chat_id} {habit.pk}").exists():
            logger.info("Задача добавлена")
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=habit.period,
                period=IntervalSchedule.DAYS,
            )
            text = f"Я буду {habit.action} в {habit.time} в {habit.place}"
            start_time = timezone.make_aware(
                datetime.combine( timezone.localdate(), habit.time ),
                timezone.get_current_timezone(),
            )
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"Send message {habit.user.chat_id} {habit.pk}",
                task="habit.tasks.send_message",
                args=json.dumps([text, habit.user.chat_id]),
                start_time=start_time,
            )

@shared_task
def send_message(text, chat_id):
    params = {"chat_id": chat_id, "text": text}
    requests.get(f"https://api.telegram.org/bot{TG_API_KEY}/sendMessage", params=params).json()