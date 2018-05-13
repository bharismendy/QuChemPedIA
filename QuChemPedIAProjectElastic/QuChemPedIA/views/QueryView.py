from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.models.QueryModel import Query
from QuChemPedIA.search import *
from django.http.response import HttpResponseRedirect
from django.urls import reverse


def query(request):
    form = QueryForm(request.GET or None)
    results = None
    try:
        # switch on what we are looking for
        if 'CID' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(cid__contains=int(request.GET.get('search'))))

        if 'IUPAC' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(iupac=request.GET.get('search')))

        if 'InChi' in request.GET.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            results = search_inchi(inchi_value=request.GET.get('search'))

        if 'Formula' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(formula=request.GET.get('search')))

        if 'SMILES' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(smiles=request.GET.get('search')))

        if 'id_log' in request.GET.get('typeQuery'):
            url = reverse('details', kwargs={'id': request.GET.get('search'), })
            return HttpResponseRedirect(url)

        if 'homo_alpha_energy' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(homo_alpha_energy=request.GET.get('search')))

        if 'homo_beta_energy' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(homo_beta_energy=request.GET.get('search')))

        if 'lumo_alpha_energy' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(lumo_alpha_energy=request.GET.get('search')))

        if 'lumo_beta_energy' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(lumo_beta_energy=request.GET.get('search')))

    except Exception as error:
        print("error :")
        print(error)

    # if we have only one result we display the details of the molecule
    if results is None:
        results = {}

    test_result = json.loads(results)
    if len(test_result) == 1:
        url = reverse('details', kwargs={'id': int(test_result["0"][0]["id_log"])})
        return HttpResponseRedirect(url)
    return render(request, 'QuChemPedIA/query.html', {'results': results, 'form': form})
