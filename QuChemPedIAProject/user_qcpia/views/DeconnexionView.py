from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def deconnexion(request):
    """view to disconnect the user"""
    try:
        logout(request)
    except Exception as error:
        print(error)
    return HttpResponseRedirect(reverse('accueil'))
