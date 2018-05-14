from django.shortcuts import render
from QuChemPedIA.search import *


<<<<<<< HEAD
@api_view(['GET', ])
@renderer_classes(( TemplateHTMLRenderer))
=======
>>>>>>> 2329d92af7b60799bd6ee76fc3a75d498172a590
def details(request, id):
    # function that show details of molecule
    results = search_id(id)
    return render(request, 'QuChemPedIA/details.html', {'results': results})


