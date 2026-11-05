from datetime import timedelta

from django.core.validators import MaxValueValidator
from rest_framework import serializers

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            "time_to_action": {
                "validators": [MaxValueValidator( timedelta(seconds=120) )]
            }
        }

    def validate(self, data):
        is_pleasant = data.get( "is_pleasant", False )
        associated_habit = data.get( "associated_habit" )
        reward = data.get( "reward" )


        if associated_habit and reward:
            raise serializers.ValidationError("Одновременно связанная прывычка и вознаграждение запрещено.")

        return data

    def validate_time_to_action(self, value):
        pass