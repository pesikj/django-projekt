from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from django.contrib.auth.models import Permission

from crm.models import Company, Opportunity


class CRMViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('jirka', 'jirka@mojefirma.cz', 'tajne-heslo')
        Company.objects.create(name="Test company", phone_number="723 000000", identification_number="1000000")
        self.user.user_permissions.add(Permission.objects.get(codename='add_opportunity'))

    def test_get_company_create(self):
        self.client.login(username='jirka', password='tajne-heslo')
        response = self.client.get(reverse('company_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_company_create(self):
        self.client.login(username='jirka', password='tajne-heslo')
        response = self.client.post(reverse('company_create'),
                                    data={"name": "Test 2",
                                          "status": "N",
                                          "phone_number": "723 123456",
                                          "identification_number": "123456789"},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Company.objects.count(), 2)

    def test_company_list(self):
        self.client.login(username='jirka', password='tajne-heslo')
        response = self.client.get(reverse("company_list"))
        self.assertContains(response, "Test company")

    def test_company_list_not_signed(self):
        response = self.client.get(reverse("company_list"), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/company/list')

    def test_create_opportunity(self):
        self.client.login(username='jirka', password='tajne-heslo')

        response = self.client.post(reverse('opportunity_create'),
                                    data={"company": 1,
                                          "sales_manager": 1,
                                          "description": "Test",
                                          "status": "1"},
                                    follow=True)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Opportunity.objects.count(), 1)