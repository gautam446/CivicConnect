from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, blank=True)
    def __str__(self): return self.name

class Complaint(models.Model):
    STATUS = (("submitted", "Submitted"), ("verified", "Verified"), ("in_progress", "In Progress"), ("resolved", "Resolved"), ("rejected", "Rejected"))
    PRIORITY = (("low", "Low"), ("medium", "Medium"), ("high", "High"))
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="complaints")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="complaints")
    title = models.CharField(max_length=160)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="complaints/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="submitted")
    priority = models.CharField(max_length=10, choices=PRIORITY, default="medium")
    assigned_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_complaints")
    staff_remarks = models.TextField(blank=True)
    reward_awarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"#{self.id} {self.title}"
