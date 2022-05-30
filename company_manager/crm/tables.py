import django_tables2 as tables
from django_tables2.utils import A
from crm.models import Opportunity, Company

class OpportunityTable(tables.Table):
    company = tables.LinkColumn("opportunity_update", args=[A("pk")], attrs={"a": {"class": "cell-with-link"}})
    class Meta:
        model = Opportunity
        fields = ("company", "sales_manager", "status", "value", "update_on")
class CompanyTable(tables.Table):
    name = tables.LinkColumn("company_update", args=[A("pk")], attrs={"a": {"class": "cell-with-link"}})
    class Meta:
        model = Company
        fields = ["name", "status", "phone_number", "identfication_number"]

