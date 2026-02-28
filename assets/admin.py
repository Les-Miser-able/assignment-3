from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Asset, Department, MaintenanceLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	"""Custom admin for the extended User model including department and manager flag."""

	fieldsets = BaseUserAdmin.fieldsets + (
		("Organization", {"fields": ("department", "is_manager")}),
	)

	list_display = BaseUserAdmin.list_display + ("department", "is_manager")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ("name",)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
	list_display = ("name", "asset_type", "cost", "repair_cost", "assigned_to", "created_at")


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
	list_display = ("asset", "date_repaired", "description", "cost")