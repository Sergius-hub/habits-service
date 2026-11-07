from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    # CRUD пользователей
    path('user/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('user/list/', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/get/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='users-update'),
    path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='users-delete'),
]