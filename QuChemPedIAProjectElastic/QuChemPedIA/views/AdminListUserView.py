from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import Utilisateur
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def list_of_all_user(request):
    """
    controler of the template admin which list all registred
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')

    query_form = QueryForm(request.GET or None)
    page = request.GET.get('page', 1)

    try:  # get all imported  file
        list_of_user = Utilisateur.objects.all()
        paginator = Paginator(list_of_user.order_by("id"), 10)
    except Exception as error:
        print(error)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.GET and 'button-search' in request.GET:
        if query_form.is_valid():
            return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/user_list.html', {'query_form': query_form, 'users': users})
