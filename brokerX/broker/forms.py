from django import forms
from django.forms.widgets import PasswordInput


class UserCreationForm(forms.Form):
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    birth_date = forms.DateField(
        label="Date of birth", widget=forms.DateInput(attrs={"type": "date"})
    )
    email = forms.EmailField(label="Email address")
    confirm_email = forms.EmailField(label="Confirm email")
    phone_number = forms.CharField(
        label="Phone number",
        max_length=20,
    )

    address = forms.CharField(label="Address", max_length=100)
    communication_method = forms.ChoiceField(
        label="Preferred communication method",
        choices=[("EM", "Email"), ("SMS", "SMS")],
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=PasswordInput(
            render_value=True,
            attrs={
                "pattern": "^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",
                "title": "Must be at least 8 characters, include one uppercase letter, one number, and one special character.",
            },
        ),
    )

    confirm_password = forms.CharField(
        label="Confirm password",
        max_length=100,
        widget=PasswordInput(
            render_value=True,
            attrs={
                "pattern": "^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",
                "title": "Must be at least 8 characters, include one uppercase letter, one number, and one special character.",
            },
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email", "")
        confirm_email = cleaned_data.get("confirm_email", "")

        if email != confirm_email:
            raise forms.ValidationError("The emails must match")


class ClientLoginForm(forms.Form):
    email = forms.EmailField(label="Email address")
    password = forms.CharField(
        label="Password",
        max_length=100,
    )
