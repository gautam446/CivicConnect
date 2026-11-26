from rest_framework.permissions import BasePermission, SAFE_METHODS

class ComplaintAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == "admin":
            return True
        if user.role == "staff":
            return obj.assigned_staff_id == user.id
        return obj.citizen_id == user.id
