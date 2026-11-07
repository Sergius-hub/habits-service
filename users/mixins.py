class OwnerQuerysetMixin:
    """Класс миксин, определяет вывод только своей информации."""

    owner_field = "user"

    def get_queryset(self):
        """Переопределяем query set для вывода только своих записей."""

        qs = super().get_queryset()
        user = self.request.user

        # Пользователь не аутентифицирован
        if not user.is_authenticated:
            return qs.none()

        # Админ видит всех
        if user.is_staff or user.is_superuser:
            return qs

        # Остальные — только себя
        return qs.filter(**{self.owner_field: user})