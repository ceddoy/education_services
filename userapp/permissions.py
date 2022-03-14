from rest_framework.permissions import BasePermission


class ForNotAuthUserPermission(BasePermission):
    """Авторизированный пользователь не может совершать регистрацию"""
    def has_permission(self, request, view) -> bool:
        return not bool(request.user and request.user.is_authenticated)
