from django.shortcuts import render
from query_qcpia.forms.QueryForm import QueryForm
from common_qcpia.search import *
from django.http.response import HttpResponseRedirect
from common_qcpia.QuChemPedIA_lib import build_url


def query(request):
    """
    controler that make research on different condition
    :param request: environment variable that contains arguement of the research
    :return: template html with dictionnary of value to display
    """
    query_form = QueryForm(request.GET or None)
    results = None
    try:
        page = int(request.GET.get('page'))
    except Exception as error:
        print(error)
        page = 1

    try:
        nbrpp = int(request.GET.get('nbrpp'))  # nombre de résultat par page
    except Exception as error:
        print(error)
        nbrpp = 10

    try:
        # switch on what we are looking for
        if 'CID' in request.GET.get('typeQuery'):
            results = search_cid(cid_value=request.GET.get('search'), nbrpp=nbrpp, page=page)

        if 'IUPAC' in request.GET.get('typeQuery'):
            results = search_iupac(iupac_value=request.GET.get('search'), nbrpp=nbrpp, page=page)

        if 'InChi' in request.GET.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            results = search_inchi(inchi_value=request.GET.get('search'), nbrpp=nbrpp, page=page)

        if 'Formula' in request.GET.get('typeQuery'):
            results = search_formula(formula_value=request.GET.get('search'), nbrpp=nbrpp, page=page)

        if 'SMILES' in request.GET.get('typeQuery'):
            results = search_smiles(smiles_value=request.GET.get('search'), nbrpp=nbrpp, page=page)

        if 'id_log' in request.GET.get('typeQuery'):
            # if we want to access to an id we forward it to the details page as a parameter
            url = build_url('details', get={'id': request.GET.get('search')})
            return HttpResponseRedirect(url)
        if 'id_user' in request.GET.get('typeQuery'):
            results = search_id_user(id_user=request.GET.get('search'), nbrpp=nbrpp, page=page)

    except Exception as error:
        print("error :")
        print(error)

    # if we have only one result we display the details of the molecule
    if results is None:
        results = '{"nbresult":0}'
    test_result = json.loads(results)
    if test_result['nbresult'] == 0 or len(test_result) == 1:
        results = '{}'
        test_result = json.loads(results)
    if len(test_result) == 2 and 'id_user' not in request.GET.get('typeQuery'):
        # if we have only one result we forward it to the detail page
        url = build_url('details', get={'id': str(test_result["0"][0]["id_log"])})
        return HttpResponseRedirect(url)

    return render(request, 'query_qcpia/query.html', {'results': test_result, 'query_form': query_form})
