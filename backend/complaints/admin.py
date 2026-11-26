from django.contrib import admin
from .models import Category, Complaint

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "citizen", "category", "status", "priority", "assigned_staff", "reward_awarded", "created_at")
    list_filter = ("status", "priority", "category", "created_at")
    search_fields = ("title", "description", "location", "citizen__username")
    list_editable = ("status", "priority", "assigned_staff")
