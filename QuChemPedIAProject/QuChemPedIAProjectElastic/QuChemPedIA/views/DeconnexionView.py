from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def deconnexion(request):
    """view to disconnect the user"""
    try:
        logout(request)
    except Exception as error:
        print(error)
    return HttpResponseRedirect('accueil')
