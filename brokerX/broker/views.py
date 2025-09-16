from django.shortcuts import render

from broker.forms import AccountCreationForm

def display_login(request):
   return render(request, "login.html")

def create_account(request):
    if request.method == "POST":
      form = AccountCreationForm(request.POST)

      if form.is_valid():
         print("Great!")

    else:
      form = AccountCreationForm()

    return render(request, "account_creation.html", {"form": form})