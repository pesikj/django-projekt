from django.forms import CharField, ModelForm
from crm.models import Employee, Company
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, Submit

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ('department', 'phone_number')


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ["name", "status", "identification_number", "email", "phone_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div("name", css_class="col-4"),
                Div("status", css_class="col-2"),
                Div("identification_number", css_class="col-2"),
                Div("email", css_class="col-3"),
                Div("phone_number", css_class="col-3"),
                css_class="row"
            ),
            ButtonHolder(
                Submit("submit", "Submit", css_class="button")
            )
        )

class RegisterUserForm(UserCreationForm):
    username = CharField(label="Email")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

