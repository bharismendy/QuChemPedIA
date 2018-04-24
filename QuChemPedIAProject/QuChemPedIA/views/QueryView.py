from django.shortcuts import render, get_list_or_404
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.models.QueryModel import Query
from django.urls import reverse
from django.http.response import HttpResponseRedirect


def query(request):
    form = QueryForm(request.POST or None)
    results = []
    try:
        #switch on what we are looking for
        if 'CID' in request.POST.get('typeQuery'):
            results =list(Query.objects.filter(cid__contains=int(request.POST.get('search'))))

        if 'IUPAC' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(iupac=request.POST.get('search')))

        if 'InChi' in request.POST.get('typeQuery'):
            #here we looking for inchi wich contain a part of what we looking for
            results = list(Query.objects.filter(inchi__contains=request.POST.get('search')))
        if 'Formula' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(formula=request.POST.get('search')))

        if 'SMILES' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(smiles=request.POST.get('search')))
    except:
        print("error in database")

    #if we have only on result we display the details of the molecule
    """if len(results) == 1:
        url = reverse('details', kwargs={'id': results[0].id})
        return HttpResponseRedirect(url)"""
    return render(request, 'QuChemPedIA/query.html', locals())
