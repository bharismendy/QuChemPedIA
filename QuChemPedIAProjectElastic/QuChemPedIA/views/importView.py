from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from QuChemPedIA.models import ImportFile
from QuChemPedIA.models import Software
from QuChemPedIA.models import SoftwareVersion
from QuChemPedIA.models import ImportRule
from QuChemPedIA.QuChemPedIA_lib import import_file
from QuChemPedIA.QuChemPedIA_lib import store_in_temp
import datetime
import json


def is_json(path):
    """
    return true if the file can be load as a json
    :param path: path to the file
    :return: boolean
    """
    with open(path) as jsonfile:
        try:
            json.load(jsonfile)
        except Exception as error:
            print(error)
            return False
        return True


def register_soft_and_version(path_to_file_to_register):
    """
    this method try to know what to do with a json file
    :param path_to_file_to_register: path to the json that could be processed
    :return: 0 for error, 1 for manual, 2 for automatic
    """
    if is_json(path = path_to_file_to_register):
        #  on récupère les information pour enregistrer la machine à état
        jsonfile = open(path_to_file_to_register)
        loaded_json = json.load(jsonfile)
        try:
            name_software = loaded_json['comp_details']['general']['package'].strip()
        except Exception as error:
            print("error for getting the software : ")
            print(error)
            return 0
        # try to register the software
        try:
            # we check if it's already exist, if not we register it
            soft, created = Software.objects.get_or_create(name=name_software)
        except Exception as error:
            print("error for registering the software : ")
            print(error)
            return 0

        try:
            version_software = loaded_json['comp_details']['general']['package_version'].strip()
        except Exception as error:
            print("error for getting the version of the software : ")
            print(error)
            return 0

        # try to register the version of the software
        try:
            # we check if it's already exist, if not we register it
            soft_vers, created = SoftwareVersion.objects.get_or_create(version_number=version_software,
                                                                       id_software=soft)
        except Exception as error:
            print("error for registering the version of the software : ")
            print(error)
            return 0

        # try to register the new rules
        try:
            # we check if it's already exist, if not we register it
            rule, created = ImportRule.objects.get_or_create(id_version=soft_vers, id_software=soft)
        except Exception as error:
            print("error for registering the new rule : ")
            print(error)
            return 0
        if rule.rule == "manual":
            return 1
        elif rule.rule == "automatic":
            return 2


def import_view(request):
    """
    controler of the template account that allow the user to import file
    :param request: variable wich contains the value of the page
    :return: template html
    """
    path_prefix = 'media/'
    if request.method == 'POST':
        myfile = request.FILES['file']
        #todo add json transform
        if is_json(myfile):
            temps = ImportFile.objects.create(path_file=path_prefix, id_user=request.user)  # register in database
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
            code_return_pol = register_soft_and_version(path_prefix+final_path)
            if code_return_pol == 0:
                temps.status = "error_0"
            if code_return_pol == 2:
                #  automatic import
                import_file.Command.import_file(path=path_prefix+final_path)
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/import.html', {'query_form': query_form})
