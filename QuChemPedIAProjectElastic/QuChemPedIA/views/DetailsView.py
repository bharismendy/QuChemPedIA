from django.shortcuts import render
from QuChemPedIA.search import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', ])
def details(request, id):
    # function that show details of molecule
    result = search_id(id=id)
    print("hel")
    return Response(result)
    #return render(request, 'QuChemPedIA/details.html', locals())

