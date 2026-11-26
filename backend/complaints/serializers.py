from rest_framework import serializers
from .models import Category, Complaint

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ComplaintSerializer(serializers.ModelSerializer):
    citizen_name = serializers.CharField(source="citizen.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    assigned_staff_name = serializers.CharField(source="assigned_staff.username", read_only=True)
    class Meta:
        model = Complaint
        fields = "__all__"
        read_only_fields = ("citizen", "status", "reward_awarded", "created_at", "updated_at")
