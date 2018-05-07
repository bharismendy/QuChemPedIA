from django.shortcuts import render
from QuChemPedIA.search import *
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer


@api_view(['GET', ])
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def details(request, id):
    # function that show details of molecule
    result = search_id(id)
    return Response(data=result, template_name='QuChemPedIA/details.html')

