from django.urls import include, path

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("opportunities", views.OpportunityViewSet)
router.register("companies", views.CompanyViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('company/create', views.CompanyCreateView.as_view(), name='company_create'),
    path('company/list', views.CompanyListView.as_view(), name='company_list'),
    path('opportunity/list', views.OpportunityListView.as_view(), name='opportunity_list'),
    path('opportunity/create', views.OpportunityCreateView.as_view(), name='opportunity_create'),
    path('opportunity/update/<int:pk>', views.OpportunityUpdateView.as_view(), name='opportunity_update'),
    path('employee/update', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path("register", views.RegisterView.as_view(), name="register"),
    path("api/", include(router.urls))
]
