from django.shortcuts import render
from query_qcpia.forms.QueryForm import QueryForm
from common_qcpia.search import *
from django.http.response import HttpResponse
import json
import base64
import os
from django.conf import settings
from user_qcpia.models import Utilisateur


def details(request):
    """
    function that return the json of a molecule
    :param request: request environment variable
    :param id: id of the json that we want to show
    :return: html template
    """
    query_form = QueryForm(request.GET or None)
    site_url = settings.SITE_URL
    port_number = settings.SITE_PORT
    return render(request, 'query_qcpia/details.html', {'query_form': query_form,
                                                        'site_url': site_url,
                                                        'port_number': port_number})


def details_json(request):
    """
    function that return the json of a molecule to an ajax request
    :param request: request environment variable
    :param id: id of the json that we want to show but could be a file
    :return: json file
    """
    id_file = request.GET.get(key='id_file')
    results = None
    path = settings.MEDIA_ROOT+'/'+ id_file
    if request.is_ajax():
        if os.path.isfile(path):
            try:
                json_data = open(path)
                results = json.load(json_data)  # deserialize it
                json_data.close()
            except Exception as error:
                print(error)
        else:
            try:
                results = search_id(id_file)
            except Exception as error:
                print(error)
    return HttpResponse(json.dumps(results), content_type="application/json")


def details_image(request):
    """
    function that return a png of a molecule to an ajax/post request
    :param request: request environment variable
    :param id: id of the molecule that we want to show
    :return: png file
    """
    id_file = request.GET.get(key='id_file')
    name_img = request.GET.get(key='name_img')
    elastic_base_dir = settings.DATA_DIR_ROOT
    for c in id_file:
        elastic_base_dir = os.path.join(elastic_base_dir, c)
    img_path = os.path.join(elastic_base_dir, name_img)
    if request.is_ajax():
        if os.path.isfile(img_path):
            image_data = base64.b64encode(open(img_path, "rb").read())
        else:
            image_data = base64.b64encode(open("/var/www/html/QuChemPedIA/static/image_test.png", "rb").read())
        return HttpResponse(image_data, content_type="image/png")


def details_author(request):
    """
    function that return the name of the author
    :param request: request environment variable
    :param id: id of the user
    :return: png file
    """
    id_author = request.GET.get(key='id_author')
    if request.is_ajax() and id_author:
        try:
            user = Utilisateur.objects.get(id=id_author)
            results = {'name': str(user.first_name)+' '+str(user.last_name)}
        except Exception as error:
            print(error)
            results = None
        return HttpResponse(json.dumps(results), content_type="application/json")
