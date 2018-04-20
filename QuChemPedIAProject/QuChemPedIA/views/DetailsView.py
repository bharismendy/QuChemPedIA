from django.shortcuts import render, get_object_or_404
from QuChemPedIA.models.QueryModel import Query
from django.http.response import HttpResponse
import os

def details(request,id):
    #function that show details on of molecule
    result = get_object_or_404(Query, id=id)
    return render(request, 'QuChemPedIA/details.html', locals())

