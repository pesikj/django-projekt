from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
import crm.models as models
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from crm.forms import EmployeeForm, UserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from crm.forms import RegisterUserForm, CompanyForm
from crm.serializers import OpportunitySerializer, CompanySerializer
from rest_framework import viewsets
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
import crm.tables as tables
import crm.filters as filters

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = models.Opportunity.objects.filter(value__isnull=False)\
            .values('status').annotate(value=Sum('value'))
        return context

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CompanyForm
    template_name = "company/create_company.html"
    success_url = reverse_lazy("index")
    # Translators: This message is shown after successful creation of a company
    success_message = _("Company created!")

class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Company
    template_name = "company/update_company.html"
    form_class = CompanyForm
    success_url = reverse_lazy("index")
    success_message = "Company updated!"

class CompanyListView(LoginRequiredMixin, SingleTableView):
    model = models.Company
    template_name = "company/list_company.html"
    table_class = tables.CompanyTable

from django.db.models import Sum
class OpportunityListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = models.Opportunity
    table_class = tables.OpportunityTable
    template_name = "opportunity/list_opportunity.html"
    filterset_class = filters.OpportunityFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs"] = self.object_list.filter(value__isnull=False).values("company__name").annotate(value=Sum("value"))
        return context


class OpportunityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    model = models.Opportunity
    template_name = "opportunity/create_opportunity.html"
    fields = ["company", "sales_manager", "primary_contact", "description", "status"]
    success_url = reverse_lazy("index")
    success_message = "Opportunity created!"

class OpportunityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Opportunity
    template_name = "opportunity/update_opportunity.html"
    fields = ["company", "primary_contact", "description", "status"]
    success_url = reverse_lazy("index")
    success_message = "Opportunity updated!"


class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "employee/update_employee.html"
    fields = ['department', 'phone_number', "office_number", "manager"]
    success_url = reverse_lazy("employee_update")
    success_message = "Data was updated successfully!"

    def get_object(self, queryset=None):
        return self.request.user.employee


class RegisterView(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = models.Opportunity.objects.all()
    serializer_class = OpportunitySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = CompanySerializer
