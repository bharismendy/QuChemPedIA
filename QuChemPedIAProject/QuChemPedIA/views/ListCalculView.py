from django.shortcuts import render, get_object_or_404
from QuChemPedIA.models.QueryModel import Query
import os


def clean (list,to_keep):
    for element in list:
        if not to_keep in element:
            list.remove(element)
    return list

def calcul (request,id):
    result = get_object_or_404(Query, id=id)
    compute_file = os.listdir(result.Path)
    compute_file = clean(list= compute_file, to_keep ='.json')#arg : type of file to keep
    compute_file = [element.replace('.json', '') for element in compute_file]

    print(compute_file)
    return render(request, 'QuChemPedIA/ListCalcul.html', locals())