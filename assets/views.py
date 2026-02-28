from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Sum, Count, F, Q

from .forms import CustomUserCreationForm
from .models import Asset, Department, MaintenanceLog
from .mixins import ManagerRequiredMixin

# TOPIC 5: Class-Based Views (CBVs) & TOPIC 4: Aggregation
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "assets/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aggregation: Calculate total value of all assets
        total_cost = Asset.objects.aggregate(total=Sum('cost'))['total'] or 0
        context['total_asset_value'] = total_cost

        # Annotation/Count: Assets per type
        context['assets_by_type'] = Asset.objects.values('asset_type').annotate(count=Count('id'))

        # Aggregation: Total asset cost grouped by department of the assigned user
        # This annotates each Department with the sum of costs for its users' assets.
        cost_by_department = (
            Department.objects
            .annotate(total_cost=Sum('users__assets__cost'))
            .filter(total_cost__isnull=False)
        )

        context['cost_by_department'] = cost_by_department
        
        return context

# TOPIC 3: Optimize SQL Queries
class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets/asset_list.html"
    context_object_name = "assets"

    def get_queryset(self):
        # Optimization: Use select_related to fetch the 'assigned_to' User 
        # in the same query, preventing the N+1 problem.
        return (
            Asset.objects
            .select_related('assigned_to')
            .annotate(repair_total=Sum('maintenance_logs__cost'))
        )

class AssetCreateView(ManagerRequiredMixin, CreateView):
    model = Asset
    template_name = "assets/asset_form.html"
    fields = ['name', 'asset_type', 'cost', 'assigned_to']
    success_url = reverse_lazy('asset-list')

    def form_valid(self, form):
        print(f"Creating asset: {form.instance.name}")
        return super().form_valid(form)
    
class AssetUpdateView(ManagerRequiredMixin, UpdateView):
    model = Asset
    template_name = "assets/asset_form.html"
    fields = ['name', 'asset_type', 'cost', 'assigned_to']
    success_url = reverse_lazy('asset-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context

class AssetDeleteView(ManagerRequiredMixin, DeleteView):
    model = Asset
    template_name = 'assets/asset_confirm_delete.html'
    success_url = reverse_lazy('asset-list')


class MaintenanceCreateView(ManagerRequiredMixin, CreateView):
    model = MaintenanceLog
    template_name = "assets/asset_form.html"
    fields = ["description", "cost", "date_repaired"]

    def form_valid(self, form):
        asset = Asset.objects.get(pk=self.kwargs["pk"])
        form.instance.asset = asset
        response = super().form_valid(form)
        # After logging maintenance, send the user back to the asset list.
        self.success_url = reverse_lazy("asset-list")
        return response

    def get_success_url(self):
        return self.success_url

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'