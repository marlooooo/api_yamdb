from django.conf import settings

# не обязательно, но желательно оставить, нужно для проверки агрумента функции
User = settings.AUTH_USER_MODEL


def get_role_permission_level(user: User) -> int:
    """Возвращает уровень доступа пользователя."""
    # Хотел сделать доп проверку на user.is_stuff, но решил проверять не здесь
    return int(user.get_role_display())
