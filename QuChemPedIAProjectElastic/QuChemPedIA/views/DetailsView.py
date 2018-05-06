from django.shortcuts import render, get_object_or_404
from QuChemPedIA.models.QueryModel import Query
from QuChemPedIA.search import *

def details(request,id):
    #function that show details on of molecule
    result = search_id(id=id)
    return render(request, 'QuChemPedIA/details.html', locals())

