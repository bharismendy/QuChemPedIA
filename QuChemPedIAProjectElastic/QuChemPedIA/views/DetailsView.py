from django.shortcuts import render
from QuChemPedIA.search import *


def details(request, id):
    """
    function that return the json of a molecule
    :param request: request environment variable
    :param id: id of the json that we want to show
    :return: html template
    """
    results = search_id(id)
    return render(request, 'QuChemPedIA/details.html', {'results': results, 'cid': id})


