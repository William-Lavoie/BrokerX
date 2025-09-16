from django.shortcuts import render

from broker.forms import AccountCreationForm
from .adapters.test_account_repository import TestAccountRepository
from .services.commands.create_account_command import CreateAccountCommand
from .services.create_account_use_case import CreateAccountUseCase

def display_login(request):
   return render(request, "login.html")

def create_account(request):
    if request.method == "POST":
      form = AccountCreationForm(request.POST)
      print("HAH")
      if form.is_valid():
        print("Great!")
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        address = form.cleaned_data["address"]
        birth_date = form.cleaned_data["birth_date"]
        phone_number = form.cleaned_data["phone_number"]
        email = form.cleaned_data["email"]

        command = CreateAccountCommand(
           first_name=first_name,
           last_name=last_name,
           address=address,
           birth_date=birth_date,
           email=email,
           phone_number=phone_number
        )

        #TODO: add dependency injections to reduce coupling between view and repositories
        use_case = CreateAccountUseCase(TestAccountRepository())
        use_case.execute(command)
      else:
         print(form.errors)
    else:
      form = AccountCreationForm()

    return render(request, "account_creation.html", {"form": form})