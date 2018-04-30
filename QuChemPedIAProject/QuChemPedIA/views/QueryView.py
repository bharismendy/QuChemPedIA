from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.models.QueryModel import Query
from datetime import datetime

def query(request):
    form = QueryForm(request.POST or None)
    results = []
    date_dep = datetime.now()
    try:
        # switch on what we are looking for
        if 'CID' in request.POST.get('typeQuery'):
            results =list(Query.objects.filter(cid__contains=int(request.POST.get('search'))))

        if 'IUPAC' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(iupac=request.POST.get('search')))

        if 'InChi' in request.POST.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            results = list(Query.objects.filter(inchi=request.POST.get('search')))
        if 'Formula' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(formula=request.POST.get('search')))

        if 'SMILES' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(smiles=request.POST.get('search')))

        if 'id_log' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(id_log=request.POST.get('search')))
            print(results)

        if 'homo_alpha_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(homo_alpha_energy=request.POST.get('search')))

        if 'homo_beta_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(homo_beta_energy=request.POST.get('search')))

        if 'lumo_alpha_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(lumo_alpha_energy=request.POST.get('search')))

        if 'lumo_beta_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(lumo_beta_energy=request.POST.get('search')))

    except:
        print("error in database")
    date_fin = datetime.now()
    temp = date_fin-date_dep
    # if we have only on result we display the details of the molecule
    """if len(results) == 1:
        url = reverse('details', kwargs={'id': results[0].id_log})
        return HttpResponseRedirect(url)"""
    return render(request, 'QuChemPedIA/query.html', locals())
