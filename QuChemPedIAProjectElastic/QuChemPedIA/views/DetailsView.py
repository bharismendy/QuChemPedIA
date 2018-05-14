from django.shortcuts import render
from QuChemPedIA.search import *


def details(request, id):
    # function that show details of molecule
    results = search_id(id)
    return render(request, 'QuChemPedIA/details.html', {'results': results})


