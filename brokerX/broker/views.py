from django.shortcuts import render

def display_login(request):
   return render(request, "login.html")
