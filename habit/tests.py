from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(email="test@test.com")
        self.habit1 = Habit.objects.create(user=self.test_user, action="test_action")
        self.habit2 = Habit.objects.create(user=self.test_user, action="test_action")
        self.habit3 = Habit.objects.create(user=self.test_user, action="test_action")

        self.client.force_authenticate(user=self.test_user)

    def test_user_created(self):
        self.assertEqual(self.test_user.email, "test@test.com")
        self.assertEqual(self.test_user.pk, self.test_user.id)

    def test_habit_list_post(self):
        url = reverse("habit:habit-list")
        data = {"action": "test_action", "place": "test"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_list_get(self):
        url = reverse("habit:habit-list")

        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"),3)

    def test_habit_detail_get(self):
        url = reverse('habit:habit-detail', kwargs={'pk': self.habit1.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_detail_patch(self):
        url = reverse('habit:habit-detail', kwargs={'pk': self.habit1.pk})
        response = self.client.patch(url, {"place":"test_place"})
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "test_place")

    def test_habit_detail_delete(self):
        url = reverse('habit:habit-detail', kwargs={'pk': self.habit1.pk})
        response_delete = self.client.delete(url)
        response_list = self.client.get(reverse("habit:habit-list"))
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_list.json().get("count"), 2)


