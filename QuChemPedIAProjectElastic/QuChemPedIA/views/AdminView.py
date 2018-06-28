from django.http import HttpResponseRedirect


def admin(request):
    """
    controler of the template dashboard that by default redirect to the admin page
    :param request: variable wich contains the value of the page
    :return: template html
    """
    return HttpResponseRedirect('admin/user_list')
