from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CivicUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("CivicConnect details", {"fields": ("role", "phone", "address")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("CivicConnect details", {"fields": ("role", "phone", "address")}),)
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
