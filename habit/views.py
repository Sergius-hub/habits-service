from rest_framework import viewsets
from users.mixins import OwnerQuerysetMixin
from habit.models import Habit
from habit.serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated

class HabitViewSet(OwnerQuerysetMixin, viewsets.ModelViewSet):
    """
    CRUD для привычек:
    - list, retrieve, update, destroy — только свои (staff видит все)
    - create — владелец проставляется автоматически
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    # owner_field = "user" — по умолчанию

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
