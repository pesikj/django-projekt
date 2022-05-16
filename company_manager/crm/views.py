from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
import crm.models as models
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from crm.forms import EmployeeForm, UserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _

class IndexView(ListView):
    template_name = "index.html"
    model = models.BookLoan

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Company
    template_name = "company/create_company.html"
    fields = ["name", "status", "phone_number", "email", "identification_number"]
    success_url = reverse_lazy("index")
    # Translators: This message is shown after successful creation of a company
    success_message = _("Company created!")

class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company
    template_name = "company/list_company.html"

class OpportunityListView(LoginRequiredMixin, ListView):
    model = models.Opportunity
    template_name = "opportunity/list_opportunity.html"

class OpportunityCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'crm.add_opportunity'
    model = models.Opportunity
    template_name = "company/create_company.html"
    fields = ["company", "sales_manager", "primary_contact", "description", "status"]
    success_url = reverse_lazy("index")
    success_message = "Opportunity created!"

class OpportunityUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
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
