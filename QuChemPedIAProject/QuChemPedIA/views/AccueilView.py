from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect


def accueil(request):
    form = QueryForm(request.POST or None)
    if form.is_valid():
        return HttpResponseRedirect('query')
    print(form)
    return render(request, 'QuChemPedIA/accueil.html',locals())
