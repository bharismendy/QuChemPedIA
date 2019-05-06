from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
import os


def rapport(request,id):
    """
    the goal of this function is to be a controler that show a pdf file to the user
    :param request: environment variable
    :param id: id of the molecule
    :return: pdf file to display
    """
    pass
    """#function that show details on of molecule
    result = get_object_or_404(Query, id=id)
    if result:
        path_to_pdf = result.Path+"/rapport.pdf"
        if os.path.isfile(path_to_pdf):
            show_pdf = open(path_to_pdf, "rb").read()

    return HttpResponse(show_pdf, content_type="application/pdf")"""
