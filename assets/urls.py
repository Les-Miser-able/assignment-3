from django.urls import path
from .views import (
    DashboardView, 
    AssetListView, 
    AssetCreateView, 
    AssetUpdateView,
    AssetDeleteView,
    MaintenanceCreateView,
    SignUpView,
    export_assets_csv,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', AssetListView.as_view(), name='asset-list'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('update/<int:pk>/', AssetUpdateView.as_view(), name='asset-update'),
    path('delete/<int:pk>/', AssetDeleteView.as_view(), name='asset-delete'),
    path('asset/<int:pk>/maintain/', MaintenanceCreateView.as_view(), name='asset-maintain'),
    path('export/csv/', export_assets_csv, name='export-csv'),
    path('register/', SignUpView.as_view(), name='register'),
]