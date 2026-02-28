from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.utils import timezone


class Department(models.Model):
    """Represents an organizational department (e.g., IT, HR, Sales)."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.name


# TOPIC 1: Custom User Models
class User(AbstractUser):
    """Custom user model extended with role and department information."""

    is_manager = models.BooleanField(default=False)
    
    # NEW DEPARTMENT FIELD - ForeignKey to Department, allowing null/blank for users without a department
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

# TOPIC 2: Abstract Base Classes (Code Reuse)
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Asset(TimeStampedModel):
    """
    Concrete model inheriting from TimeStampedModel.
    """
    ASSET_TYPES = (
        ('LAPTOP', 'Laptop'),
        ('MONITOR', 'Monitor'),
        ('PHONE', 'Phone'),
        ('FURNITURE', 'Furniture'),
    )

    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    # DecimalField is best practice for currency/value
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total repair cost accumulated for this asset.") 
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"


class MaintenanceLog(models.Model):
    """Represents a single maintenance or repair event for an asset."""

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="maintenance_logs",
    )
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_repaired = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-date_repaired", "-id"]

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return f"Maintenance for {self.asset} on {self.date_repaired}"