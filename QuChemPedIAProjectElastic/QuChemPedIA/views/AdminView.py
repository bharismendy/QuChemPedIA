from django.http import HttpResponseRedirect


def admin(request):
    """
    controler of the template dashboard that by default redirect to the admin page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')
    return HttpResponseRedirect('admin/user_list')
