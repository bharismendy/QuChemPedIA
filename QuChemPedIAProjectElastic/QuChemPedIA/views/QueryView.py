from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.models.QueryModel import Query
from datetime import datetime
from QuChemPedIA.search import *
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer


@api_view(['GET', ])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer, render))
def query(request):
    form = QueryForm(request.GET or None)
    results = None
    date_dep = datetime.now()
    try:
        # switch on what we are looking for
        if 'CID' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(cid__contains=int(request.GET.get('search'))))

        if 'IUPAC' in request.GET.get('typeQuery'):
            results = list(Query.objects.filter(iupac=request.GET.get('search')))

        if 'InChi' in request.GET.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            # results = list(Query.objects.filter(inchi=request.GET.get('search')).order_by('id_log')[:25])
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
    date_fin = datetime.now()
    temp = date_fin-date_dep
    # if we have only one result we display the details of the molecule
    if results is None:
        results = {}
    if len(results) == 1:
        url = reverse('details', kwargs={'id': results[0].id_log})
        return HttpResponseRedirect(url)
    Response(data=results, template_name='QuChemPedIA/query.html')
    return render(request, 'QuChemPedIA/query.html', locals())
