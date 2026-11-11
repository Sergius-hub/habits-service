from datetime import timedelta
from rest_framework import serializers
from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "action",
            "place",
            "time",
            "time_to_action",
            "reward",
            "associated_habit",
            "is_published"
        )
        read_only_fields = ("id", "user")

    def validate(self, data):

        associated_habit = data.get( "associated_habit" )
        reward = data.get( "reward" )
        is_pleasant = data.get("is_pleasant", False)

        if associated_habit and reward:
            raise serializers.ValidationError(
                "Одновременная запись полей связанная привычка и вознаграждение исключено."
            )

        if is_pleasant and (associated_habit is not None or reward is not None):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        return data

    def validate_time_to_action(self, value):
        if value is not None and value > timedelta(seconds=120):
            raise serializers.ValidationError(
                "Время на выполнение не должно превышать 120 секунд."
            )
        return value

    def validate_associated_habit(self, value):
        if not value.is_pleasant:
            raise serializers.ValidationError(
                "Связанные привычки должны быть только приятными."
            )
        return value

    def validate_period(self, value):
        if not (1 <= value <= 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )
        return value

