from users.serializers import UserModelSerializer
from users.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.mixins import OwnerQuerysetMixin

class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    queryset = User.objects.none()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(is_active=True)

class UserListAPIView(OwnerQuerysetMixin, generics.ListAPIView):
    """Получение списка пользователей."""
    owner_field = "pk"
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAuthenticated,)

class UserRetrieveAPIView(OwnerQuerysetMixin, generics.RetrieveAPIView):
    owner_field = "pk"
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAuthenticated,)

class UserUpdateAPIView(OwnerQuerysetMixin, generics.UpdateAPIView):
    owner_field = "pk"
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAuthenticated,)

class UserDestroyAPIView(OwnerQuerysetMixin, generics.DestroyAPIView):
    owner_field = "pk"
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAuthenticated,)
