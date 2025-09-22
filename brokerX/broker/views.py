from django.http import HttpResponse
from django.shortcuts import render

from broker.forms import UserCreationForm, ClientLoginForm
from .services.create_account_use_case.verify_passcode import VerifyPassCode
from .adapters.email_otp_repository import EmailOTPRepository
from .adapters.django_client_repository import DjangoClientRepository
from .services.commands.create_client_command import CreateClientCommand
from .services.create_account_use_case.create_client import CreateClientUseCase
from django.contrib.auth import authenticate, login


def display_login(request):
    return render(request, "login.html")

def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            address = form.cleaned_data["address"]
            birth_date = form.cleaned_data["birth_date"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            command = CreateClientCommand(
                first_name=first_name,
                last_name=last_name,
                address=address,
                birth_date=birth_date,
                email=email,
                phone_number=phone_number,
                password=password
            )

            # TODO: add dependency injections to reduce coupling between view and repositories
            use_case = CreateClientUseCase(DjangoClientRepository(), EmailOTPRepository())
            use_case.execute(command)
            return render(request, "otp_confirmation.html")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, "user_creation.html", {"form": form})


def confirm_passcode(request):
    if request.method == "GET":
        return HttpResponse("Error: You can only use a POST")

    passcode = request.POST.get("passcode", "")
    use_case = VerifyPassCode(EmailOTPRepository(), DjangoClientRepository())
    use_case.execute("william.lavoie.3@ens.etsmtl.ca", passcode)

    return render(request, "otp_confirmation.html")



def client_login(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)
            if user is not None:
                print("login successfully")
                login(request, user)
                return render(request, "home_page.html", context={"name": user.first_name + " " + user.last_name, "email": user.email})
            #TODO: implement full use case
            return render(request, "otp_confirmation.html")
        else:
            print(form.errors)
    else:
        form = ClientLoginForm()

    return render(request, "login.html", {"form": form})
