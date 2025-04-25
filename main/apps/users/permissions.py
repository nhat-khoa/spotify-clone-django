# permissions.py
from rest_framework.permissions import BasePermission
from django.utils import timezone

class IsPremium(BasePermission):
    message = "Premium account required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.premium_expired and request.user.premium_expired > timezone.now()
        )
