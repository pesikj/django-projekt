from django.forms import CharField, ModelForm
from crm.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('department', 'phone_number')


class RegisterUserForm(UserCreationForm):
    username = CharField(label="Email")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

