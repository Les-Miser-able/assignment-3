from django.core.exceptions import PermissionDenied

class ManagerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            # For demo purposes, superusers are treated as managers
            if not request.user.is_superuser:
                raise PermissionDenied("You do not have manager access.")
        return super().dispatch(request, *args, **kwargs)