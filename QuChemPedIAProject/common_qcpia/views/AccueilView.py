from django.shortcuts import render, reverse
from query_qcpia.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect


def accueil(request):
    """
    controler of the template accueil.html
    :param request: variable wich contains the value of the page
    :return: template html
    """
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect(reverse('query'))
    return render(request, 'common_qcpia/accueil.html', {'query_form': query_form})

