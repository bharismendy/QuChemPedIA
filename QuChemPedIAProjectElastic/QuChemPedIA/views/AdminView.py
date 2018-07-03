from django.http import HttpResponseRedirect


def could_use_it(request):
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')


def admin(request):
    """
    controler of the template dashboard that by default redirect to the admin page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    could_use_it(request=request)
    return HttpResponseRedirect('admin/user_list')
