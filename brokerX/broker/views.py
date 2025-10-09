from decimal import ROUND_HALF_UP, Decimal

from broker.forms import ClientLoginForm, PlaceOrderForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from brokerX import settings

from .adapters.django_client_repository import DjangoClientRepository
from .adapters.django_transaction_repository import DjangoTransactionRepository
from .adapters.django_wallet_repository import DjangoWalletRepository
from .adapters.email_otp_repository import EmailOTPRepository
from .adapters.mock_payment_service_repository import MockPaymentServiceRepository
from .services.add_funds_to_wallet_use_case import (
    AddFundsToWalletUseCase,
    AddFundsToWalletUseCaseResult,
)
from .services.commands.create_client_command import CreateClientCommand
from .services.create_account_use_case.create_client import CreateClientUseCase
from .services.create_account_use_case.verify_passcode import VerifyPassCode


@login_required
def display_homepage(request):
    return render(
        request,
        "home_page.html",
        context={
            "name": request.user.first_name + " " + request.user.last_name,
            "email": request.user.email,
        },
    )


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
                password=password,
            )

            # TODO: add dependency injections to reduce coupling between view and repositories
            use_case = CreateClientUseCase(
                DjangoClientRepository(), EmailOTPRepository()
            )
            result = use_case.execute(command)
            if not result.success:
                return render(request, "user_creation.html", {"form": form})

            user = authenticate(request, username=email, password=password)
            login(request, user)

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
    use_case.execute(request.user.email, passcode)

    return render(
        request,
        "home_page.html",
        context={
            "name": request.user.first_name + " " + request.user.last_name,
            "email": request.user.email,
        },
    )


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
                return render(
                    request,
                    "home_page.html",
                    context={
                        "name": user.first_name + " " + user.last_name,
                        "email": user.email,
                    },
                )
            # TODO: implement full use case
            return display_homepage(request)
        else:
            print(form.errors)
    else:
        form = ClientLoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def client_logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


@login_required
def display_wallet(request):
    use_case = AddFundsToWalletUseCase(
        DjangoClientRepository(),
        MockPaymentServiceRepository(),
        DjangoWalletRepository(),
        DjangoTransactionRepository(),
    )
    balance = use_case.get_balance(request.user.email)
    return render(request, "wallet.html", context={"amount": balance})


@login_required
def add_funds_to_wallet(request):
    if request.method == "GET":
        return HttpResponse("Error: You can only use a POST")

    amount = request.POST.get("amount", 0.00)
    idempotency_key = request.POST.get("idempotency_key")

    if not idempotency_key:
        return render(request, "wallet.html", context={"amount": 100})

    amount = Decimal(amount).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )  # TODO: catch error

    use_case = AddFundsToWalletUseCase(
        DjangoClientRepository(),
        MockPaymentServiceRepository(),
        DjangoWalletRepository(),
        DjangoTransactionRepository(),
    )
    response: AddFundsToWalletUseCaseResult = use_case.execute(
        request.user.email, amount, idempotency_key
    )
    #  use_case.execute("william.lavoie.3@ens.etsmtl.ca", passcode)

    return render(request, "wallet.html", context={"amount": response.new_balance})


@login_required
def display_orders(request):
    if request.method == "POST":
        form = PlaceOrderForm(request.POST)

        return render(request, "orders.html", {"form": form})
    else:
        form = PlaceOrderForm()

    return render(request, "orders.html", {"form": form})
