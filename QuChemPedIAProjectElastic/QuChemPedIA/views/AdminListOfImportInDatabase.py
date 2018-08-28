from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import ImportFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def list_of_import_in_database(request):
    """
    controler of the template account that allow the user to see which calculation he contribute
    :param request: variable wich contains the value of the page
    :return: template html
    """

    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect('/QuChemPedIA/accueil')

    query_form = QueryForm(request.GET or None)
    page = request.GET.get('page', 1)
    try:  # get all imported  file
        list_imported_file = ImportFile.objects.all()
        paginator = Paginator(list_imported_file.order_by("id_file"), 10)
    except Exception as error:
        print(error)
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)
    if request.GET and 'button-search' in request.GET:
        if query_form.is_valid():
            return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/admin_list_on_import_in_database.html', {'query_form': query_form,
                                                                                 "history": history,
                                                                                 "media": media})
