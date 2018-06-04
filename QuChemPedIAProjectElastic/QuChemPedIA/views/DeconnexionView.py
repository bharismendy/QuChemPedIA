from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from .AuthView import connexion


def deconnexion(request):
    logout(request)
    return redirect(reverse(viewname=connexion))