from django.contrib import admin
import crm.models

class CompanyAdmin(admin.ModelAdmin):
    fields = ["name", "status", "phone_number", "email", "address", "identification_number"]
    readonly_fields = ["status", "identification_number"]
    list_display = ["name", "status", "email"]
    list_filter = ["status"]
    search_fields = ["name", "email", "identification_number", "opportunity__description"]

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ["status", "value", "company"]

admin.site.register(crm.models.Company, CompanyAdmin)
admin.site.register(crm.models.Opportunity, OpportunityAdmin)
admin.site.register(crm.models.Employee)
admin.site.register(crm.models.BookLoan)
