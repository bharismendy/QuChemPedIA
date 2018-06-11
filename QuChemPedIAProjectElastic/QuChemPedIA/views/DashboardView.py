from django.http import HttpResponseRedirect


def dashboard(request):
    """
    controler of the template dashboard that by default redirect to account page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    return HttpResponseRedirect('dashboard/account')
