from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def deconnexion(request):
    try:
        logout(request)
    except Exception as error:
        print(error)
    if not request.META.get('HTTP_REFERER', '/') == '/':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect('accueil')
