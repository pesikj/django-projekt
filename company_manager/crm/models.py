import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Address(models.Model):
    street = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)


class Company(models.Model):
    status_choices = (
        ("N", "New"),
        ("L", "Lead"),
        ("O", "Opportunity"),
        ("C", "Active Customer"),
        ("FC", "Former Customer"),
        ("I", "Inactive"),
    )
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=2, default="N", choices=status_choices)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    identification_number = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    primary_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=50)


class Opportunity(models.Model):
    status_choices = (
        ("1", "Prospecting"),
        ("2", "Analysis"),
        ("3", "Proposal"),
        ("4", "Negotiation"),
        ("5", "Closed Won"),
        ("0", "Closed Lost"),
    )

    company = models.ForeignKey(Company, on_delete=models.RESTRICT)
    sales_manager = models.ForeignKey(User, on_delete=models.RESTRICT)
    primary_contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=2, default="1", choices=status_choices)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    # Tvorba atributu přesunuta z lekce do cvičení
    phone_number = models.CharField(max_length=20, blank=True)
    office_number = models.CharField(max_length=10, blank=True)
    manager = models.ForeignKey("Employee", on_delete=models.SET_NULL, null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)

@receiver(post_save, sender=Opportunity)
def create_opportunity(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Byla vytvořena nová opportunita',
            f'Byla vytvořena opportunita pro zákazníka {instance.company.name}',
            'robot@mojefirma.cz',
            ["sales_manager@czechitas.cz"]
        )

class BookLoan(models.Model):
    loan_date_time = models.DateTimeField(auto_now_add=True)
    returned_date_time = models.DateTimeField(null=True, blank=True)

    @property
    def book_return_deadline(self):
        return self.loan_date_time + datetime.timedelta(days=30)

    @property
    def delayed_error(self):
        return self.book_return_deadline < datetime.datetime.now()

    @property
    def delayed(self):
        from django.utils import timezone
        return self.book_return_deadline < timezone.now()

    @property
    def fee(self):
        if self.returned_date_time is not None and self.returned_date_time > self.book_return_deadline:
            difference = self.returned_date_time - self.book_return_deadline
            return difference.days * 20
        return 0
