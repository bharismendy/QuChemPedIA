from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def admin(request):
    """
    controler of the template dashboard that by default redirect to the admin page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))
    return HttpResponseRedirect(reverse('admin/user_list'))
