from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habit.views import HabitViewSet
from habit.apps import HabitConfig

app_name = HabitConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("", include(router.urls)),
]