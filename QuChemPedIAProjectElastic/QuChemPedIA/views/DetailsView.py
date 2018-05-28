from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.search import *
from django.http.response import HttpResponse
import json


def details(request):
    """
    function that return the json of a molecule
    :param request: request environment variable
    :param id: id of the json that we want to show
    :return: html template
    """
    query_form = QueryForm(request.GET or None)

    return render(request, 'QuChemPedIA/details.html', {'query_form': query_form})


def details_json(request,id):
    """
    function that return the json of a molecule to an ajax request
    :param request: request environment variable
    :param id: id of the json that we want to show
    :return: json file
    """
    if request.is_ajax():
        if id == "demo":
            json_data = open('QuChemPedIA/static/demo.json')
            results = json.load(json_data)  # deserialize it
            json_data.close()
        elif id == "opt":
            json_data = open('QuChemPedIA/static/OPT_only_freq_TD.json')
            results = json.load(json_data)  # deserialize it
            json_data.close()
        else :
            try:
                results = search_id(id)
            except:
                results = None
        return HttpResponse(json.dumps(results), content_type="application/json")


def details_image(request,id):
    """
    function that return the json of a molecule to an ajax request
    :param request: request environment variable
    :param id: id of the json that we want to show
    :return: json file
    """
    if request.isPost():
        image_data = open("QuChemPedIA/static/image_test.png", "rb").read()
        return HttpResponse(image_data, content_type="image/png")
