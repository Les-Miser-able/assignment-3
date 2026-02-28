"""
Seed script: populates the database with sample departments, users, assets,
and maintenance logs for demonstration purposes.

Run with:  python manage.py shell < seed_data.py
"""
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from decimal import Decimal
from datetime import date
from assets.models import Department, User, Asset, MaintenanceLog

# ── Departments ──────────────────────────────────────────────────
dept_names = ["IT", "HR", "Sales", "Finance", "Operations"]
departments = {}
for name in dept_names:
    dept, _ = Department.objects.get_or_create(name=name)
    departments[name] = dept

# ── Users ────────────────────────────────────────────────────────
user_data = [
    {"username": "alice",   "department": "IT",         "is_manager": True},
    {"username": "bob",     "department": "HR",         "is_manager": False},
    {"username": "carol",   "department": "Sales",      "is_manager": False},
    {"username": "dave",    "department": "Finance",    "is_manager": True},
    {"username": "eve",     "department": "Operations", "is_manager": False},
]
users = {}
for ud in user_data:
    user, created = User.objects.get_or_create(
        username=ud["username"],
        defaults={
            "department": departments[ud["department"]],
            "is_manager": ud["is_manager"],
        },
    )
    if created:
        user.set_password("pass1234")
        user.save()
    users[ud["username"]] = user

# ── Assets (15 minimum) ─────────────────────────────────────────
asset_data = [
    {"name": "Dell Latitude 5540",      "asset_type": "LAPTOP",    "cost": "1249.99", "assigned_to": "alice"},
    {"name": "MacBook Pro 14\"",         "asset_type": "LAPTOP",    "cost": "2399.00", "assigned_to": "carol"},
    {"name": "Lenovo ThinkPad X1",      "asset_type": "LAPTOP",    "cost": "1599.00", "assigned_to": "dave"},
    {"name": "HP EliteBook 840",        "asset_type": "LAPTOP",    "cost": "1349.50", "assigned_to": "bob"},
    {"name": "Dell UltraSharp 27\"",     "asset_type": "MONITOR",   "cost": "549.99",  "assigned_to": "alice"},
    {"name": "LG 34\" Ultrawide",        "asset_type": "MONITOR",   "cost": "699.00",  "assigned_to": "carol"},
    {"name": "Samsung 24\" FHD",         "asset_type": "MONITOR",   "cost": "229.99",  "assigned_to": "eve"},
    {"name": "iPhone 15 Pro",           "asset_type": "PHONE",     "cost": "999.00",  "assigned_to": "dave"},
    {"name": "Samsung Galaxy S24",      "asset_type": "PHONE",     "cost": "849.99",  "assigned_to": "bob"},
    {"name": "Google Pixel 8",          "asset_type": "PHONE",     "cost": "699.00",  "assigned_to": "alice"},
    {"name": "Standing Desk - Large",   "asset_type": "FURNITURE", "cost": "789.00",  "assigned_to": "eve"},
    {"name": "Ergonomic Office Chair",  "asset_type": "FURNITURE", "cost": "549.00",  "assigned_to": "carol"},
    {"name": "Conference Table 8-Seat", "asset_type": "FURNITURE", "cost": "1200.00", "assigned_to": None},
    {"name": "Dell Monitor 22\"",        "asset_type": "MONITOR",   "cost": "189.99",  "assigned_to": "bob"},
    {"name": "HP ProBook 450",          "asset_type": "LAPTOP",    "cost": "1099.00", "assigned_to": "eve"},
]

assets = {}
for ad in asset_data:
    asset, _ = Asset.objects.get_or_create(
        name=ad["name"],
        defaults={
            "asset_type": ad["asset_type"],
            "cost": Decimal(ad["cost"]),
            "assigned_to": users.get(ad["assigned_to"]),
        },
    )
    assets[ad["name"]] = asset

# ── Maintenance Logs (5 minimum) ────────────────────────────────
log_data = [
    {"asset": "Dell Latitude 5540",  "description": "Replaced faulty battery",              "cost": "129.99", "date": "2025-11-15"},
    {"asset": "MacBook Pro 14\"",     "description": "Screen replacement after drop damage",  "cost": "549.00", "date": "2025-12-02"},
    {"asset": "Samsung Galaxy S24",  "description": "Cracked screen repair",                 "cost": "249.99", "date": "2026-01-10"},
    {"asset": "Standing Desk - Large","description": "Motor replacement for height adjustment","cost": "175.00", "date": "2026-01-25"},
    {"asset": "Dell Latitude 5540",  "description": "SSD upgrade from 256 GB to 1 TB",       "cost": "89.99",  "date": "2026-02-14"},
]

for ld in log_data:
    MaintenanceLog.objects.get_or_create(
        asset=assets[ld["asset"]],
        description=ld["description"],
        defaults={
            "cost": Decimal(ld["cost"]),
            "date_repaired": date.fromisoformat(ld["date"]),
        },
    )

print(f"Seeded: {Asset.objects.count()} assets, {MaintenanceLog.objects.count()} maintenance logs")
