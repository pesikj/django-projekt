from rest_framework import serializers
from crm.models import Opportunity, Company

class OpportunitySerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    sales_manager = serializers.StringRelatedField()

    class Meta:
        model = Opportunity
        fields = ["company", "sales_manager", "status", "value"]

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "status", "identification_number", "email"]
