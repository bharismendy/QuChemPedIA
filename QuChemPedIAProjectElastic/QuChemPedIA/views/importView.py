from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import ImportFile
# from QuChemPedIA.QuChemPedIA_lib import import_file
from QuChemPedIA.QuChemPedIA_lib import store_in_temp
import datetime


def import_view(request):
    """
    controler of the template account that allow the user to import file
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if request.method == 'POST':
        myfile = request.FILES['file']
        temps = ImportFile.objects.create(path_file='media/', id_user=request.user)  # register in database
        final_path = store_in_temp(id_calcul=str(temps.id_file), file=myfile)
        temps.path_file = final_path
        temps.save()
        # adding an import  for this day to the user*
        if request.user.is_authenticated:
            if request.user.last_date_upload != datetime.datetime.today().date() \
                    or request.user.last_date_upload is None:
                request.user.last_date_upload = datetime.datetime.today()
                request.user.number_of_upload_this_day = 1
                request.user.save()
            else:
                request.user.number_of_upload_this_day += 1
                request.user.save()
            request.user.refresh_from_db()
        else:
            #   user == anonymous
            pass
        # launch import if politique == true
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/import.html', {'query_form': query_form})
