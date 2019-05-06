from django.http import HttpResponseRedirect
from django.shortcuts import reverse

def dashboard(request):
    """
    controler of the template dashboard that by default redirect to account page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    return HttpResponseRedirect(reverse('dashboard/history'))
