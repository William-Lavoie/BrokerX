from django import forms
from django.forms.widgets import TelInput, PasswordInput

class AccountCreationForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    birth_date = forms.DateField(
        label="Date of birth",
        input_formats=["%d-%m-%y"],
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(label="Email address")
    confirm_email = forms.EmailField(label="Confirm email")
    phone_number = forms.CharField(
            label="Phone number",
            max_length=20,
            widget=TelInput(attrs={
                'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{4}',
            })
        )
    communication_method = forms.ChoiceField(
        label="Preferred communication method",
        choices=[("EM", "Email"),
                  ("SMS", "SMS")]
        )
    password = forms.CharField(label="Password",
                               max_length=100,
                               widget=PasswordInput(
                                    render_value=True
                               ))

    confirm_password = forms.CharField(label="Confirm password",
                               max_length=100,
                               widget=PasswordInput(
                                    render_value=True
                               ))