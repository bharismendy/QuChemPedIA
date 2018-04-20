from django.shortcuts import render, get_object_or_404
from QuChemPedIA.models.QueryModel import Query
from django.http.response import HttpResponse
import os

def rapport(request,id):
    #function that show details on of molecule
    result = get_object_or_404(Query, id=id)
    if result:
        path_to_pdf = result.Path+"/rapport.pdf"
        if os.path.isfile(path_to_pdf):
            show_pdf = open(path_to_pdf, "rb").read()

    return HttpResponse(show_pdf, content_type="application/pdf")
