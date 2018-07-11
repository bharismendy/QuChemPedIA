from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import Utilisateur
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from QuChemPedIA.forms.AdminSearchUserForm import SearchUserForm


def list_of_all_user(request):
    """
    controler of the template admin which list all registred user and allow to find one
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')

    query_form = QueryForm(request.GET or None)
    page = request.GET.get('page', 1)
    search_user_form = SearchUserForm(request.GET or None)

    try:
        # switch on what we are looking for
        if 'ID' in request.GET.get('typeQuery'):
            list_of_user = Utilisateur.objects.filter(id=int(request.GET.get('search')))

        elif 'first_name' in request.GET.get('typeQuery'):
            list_of_user = Utilisateur.objects.filter(first_name__icontains=request.GET.get('search'))

        elif 'last_name' in request.GET.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            list_of_user = Utilisateur.objects.filter(last_name__icontains=request.GET.get('search'))

        elif 'affiliation' in request.GET.get('typeQuery'):
            list_of_user = Utilisateur.objects.filter(affiliation__icontains=request.GET.get('search'))

        elif 'mail' in request.GET.get('typeQuery'):
            list_of_user = Utilisateur.objects.filter(email__icontains=request.GET.get('search'))
        else:
            list_of_user = Utilisateur.objects.all()
        paginator = Paginator(list_of_user.order_by("id"), 10)
    except Exception as error:
        print(error)
        print("error in database")
        list_of_user = Utilisateur.objects.all()
        paginator = Paginator(list_of_user.order_by("id"), 10)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.GET and 'button-search' in request.GET:
        if query_form.is_valid():
            return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/admin_list_user.html', {'query_form': query_form,
                                                                'users': users,
                                                                'search_user_form': search_user_form})
