from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Complaint
from .serializers import CategorySerializer, ComplaintSerializer
from rewards.models import RewardTransaction

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_superuser or request.user.role == "admin"

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Complaint.objects.select_related("citizen", "category", "assigned_staff").order_by("-created_at")
        if user.is_superuser or user.role == "admin":
            return qs
        if user.role == "staff":
            return qs.filter(assigned_staff=user)
        return qs.filter(citizen=user)

    def perform_create(self, serializer):
        serializer.save(citizen=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role == "citizen" and instance.citizen_id == user.id:
            if instance.status != "submitted":
                return Response({"detail": "Only submitted complaints can be edited."}, status=400)
            allowed = {"title", "description", "location", "category", "image"}
            data = {k: v for k, v in request.data.items() if k in allowed}
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if user.role == "staff" and instance.assigned_staff_id == user.id:
            allowed = {"status", "staff_remarks"}
            data = {k: v for k, v in request.data.items() if k in allowed}
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        if user.is_superuser or user.role == "admin":
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update this complaint."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def verify(self, request, pk=None):
        complaint = self.get_object()
        if not (request.user.is_superuser or request.user.role == "admin"):
            return Response({"detail": "Admin access required."}, status=403)
        with transaction.atomic():
            complaint = Complaint.objects.select_for_update().get(pk=complaint.pk)
            if not complaint.reward_awarded:
                complaint.status = "verified"
                complaint.reward_awarded = True
                complaint.save()
                RewardTransaction.objects.create(
                    user=complaint.citizen, points=30, transaction_type="earned",
                    description=f"Verified complaint #{complaint.id}"
                )
        return Response(self.get_serializer(complaint).data)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        if not (request.user.is_superuser or request.user.role == "admin"):
            return Response({"detail": "Admin access required."}, status=403)
        complaint = self.get_object()
        staff_id = request.data.get("staff_id")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            staff = User.objects.get(pk=staff_id, role="staff", is_active=True)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"detail": "Valid active staff_id required."}, status=400)
        complaint.assigned_staff = staff
        complaint.save(update_fields=["assigned_staff", "updated_at"])
        return Response(self.get_serializer(complaint).data)
