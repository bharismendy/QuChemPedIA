from query_qcpia.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from import_qcpia.models import ImportFile, JobType, Software, SoftwareVersion, ImportRule
from common_qcpia.QuChemPedIA_lib import import_file
from common_qcpia.QuChemPedIA_lib import store_in_temp
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from common_qcpia.QuChemPedIA_lib.scanlog import process_logfile
import datetime
import json
import tempfile
import shutil
import os
from common_qcpia.QuChemPedIA_lib import build_url
from QuChemPedIAProject.settings import MEDIA_ROOT


def register_soft_job_type_and_version(path_to_file_to_register):
    """
    this method try to know what to do with a json file
    :param path_to_file_to_register: path to the json that could be processed
    :return: 0 for error, 1 for manual, 2 for automatic
    """
    #  on récupère les information pour enregistrer la machine à état
    jsonfile = open(path_to_file_to_register)
    loaded_json = json.load(jsonfile)

    # ######## software ######## #
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

    # ######## version of the software ######## #
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

    # ######## job_type ######## #
    try:
        job_type = loaded_json['comp_details']['general']['job_type']
    except Exception as error:
        print("error for getting the version of the software : ")
        print(error)
        return 0

    inserted_jt = []
    # try to register the job_type
    for job in job_type:
        try:
            # we check if it's already exist, if not we register it
                job_type_ins, created = JobType.objects.get_or_create(name=job)
                inserted_jt.append(job_type_ins)
        except Exception as error:
            print("error for registering the version of the software : ")
            print(error)
            return 0

    # ######## rule ######## #
    # try to register the new rules
    for job in inserted_jt:
        result = []
        try:
            # we check if it's already exist, if not we register it
            rule, created = ImportRule.objects.get_or_create(id_version=soft_vers,
                                                             id_software=soft,
                                                             id_job_type=job)
        except Exception as error:
            print("error for registering the new rule : ")
            print(error)
            return 0
        if rule.rule == "manual":
            result.append(1)
        elif rule.rule == "automatic":
            result.append(2)
        elif rule.rule == "delete":
            result.append(3)
        return result


def update_status_in_db(result_of_import: int, import_object: ImportFile):
    """
    this function update the status of an import in database
    :param result_of_import: an integer which contains the result of the import function
    :param import_object : current object to update
    :return: nothing
    """
    if result_of_import == 0:
        import_object.status = "imported to database"
        import_object.imported = True
    elif result_of_import == 1:
        import_object.status = "not archivable"
    elif result_of_import == 2:
        import_object.status = "theory not supported yet"
    elif result_of_import == 3:
        import_object.status = "already in database"
        import_object.imported = True
    else:
        import_object.status = "something goes wrong"
    import_object.save()





def import_view(request):
    """
    controler of the template account that allow the user to import file
    :param request: variable wich contains the value of the page
    :return: template html
    """
    path_prefix = 'media/'
    number_of_stand_by_import = 0
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect(reverse('query'))

    if request.user.is_authenticated:
        number_of_stand_by_import = len(list(ImportFile.objects.filter(id_user=request.user.id).filter(
            status="stand-by")))

    if request.method == 'POST' and 'btn_upload' in request.POST:
        if not request.FILES['file']:
            myfile = request.POST.get('file')
        else:
            myfile = request.FILES['file']  # work for dropzone only
        # todo add json transform
        content = ContentFile(myfile.read())
        #dirpath = tempfile.mkdtemp(prefix="/var/www/html/media/to_import/tmp/")
        dirpath = tempfile.mkdtemp(prefix=os.path.join(MEDIA_ROOT, "to_import/tmp/"))
        filepath = os.path.join(dirpath, "file.log")
        default_storage.save(filepath, content)
        file_list, json_list = process_logfile(filepath, log_storage_path=os.path.dirname(dirpath))

        for i, json_file in enumerate(json_list):
            temps = ImportFile.objects.create(path_file=path_prefix, log_path_file= path_prefix, id_user=request.user)  # register in database
            file_log = open(file_list[i], 'r')
            file_log_content = file_log.read()
            file_log.close()
            log_final_path = store_in_temp(id_calcul=str(temps.id_file), file=file_log_content, type='log')
            final_path = store_in_temp(id_calcul=str(temps.id_file), file=json_file, type="json")
            temps.path_file = final_path
            temps.log_path_file = log_final_path
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
            code_return_pol = register_soft_job_type_and_version(settings.BASE_DIR+settings.MEDIA_URL+final_path)
            if code_return_pol == 0:
                temps.status = "error can't define policy"
                temps.save()
            # we do nothing in case of 1 because it's define by default
            elif 3 in code_return_pol:
                os.remove(temps.path_file)
                temps.status = "import not supported yet"
                temps.save()

            elif 2 in code_return_pol:
                #  automatic import
                try:
                    path = "media/" + temps.path_file
                    update_status_in_db(result_of_import=import_file(path=file_list[i], json_file=json_file, id_user=temps.id_user.id),
                                        import_object=temps)
                except Exception as error:
                    print(error)
                    temps.status = 'import failed'
                    temps.save()

        shutil.rmtree(dirpath)
    return render(request, 'user_qcpia/user_import.html', {'query_form': query_form,
                                                           'number_of_stand_by_import': number_of_stand_by_import})


def launch_import(request, id_file, page):
    """
    controler from admin view to launch manuallly an import
    :param request: environment variable wich containt all value exchanged between client and server
    :param id_file: id of the file in DB o import in ES
    :param page: number of the page
    :return: html template
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))
    file = ImportFile.objects.get(id_file=id_file)
    path_json = settings.BASE_DIR+settings.MEDIA_URL+file.path_file
    with open(path_json, "r") as json_open:
        json_file = json.load(json_open)
    path_log = settings.BASE_DIR+settings.MEDIA_URL+file.log_path_file
    id_user = file.id_user.id
    try:
        update_status_in_db(result_of_import=import_file(path=path_log, json_file=json_file, id_user=id_user),
                            import_object=file)
    except Exception as error:
        print(error)
        file.status = 'import failed'
        file.save()
    url = build_url('admin/list_of_import_in_database', get={'page': str(page)})
    return HttpResponseRedirect(url)


def delete_import(request, id_file, page):
    """
    controler from admin view to delete manuallly an import
    :param request: environment variable wich containt all value exchanged between client and server
    :param id_file: id of the file in DB o import in ES
    :param page: number of the page
    :return: html template
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))
    file = ImportFile.objects.get(id_file=id_file)

    if os.path.isfile(path=os.path.join('/var/www/html/media/', file.path_file)):
        try:
            os.remove(path=os.path.join('/var/www/html/media/', file.path_file))
        except Exception as error:
            print(error)
            file.status("couldn't delete the import")
    if os.path.isfile(path=os.path.join('/var/www/html/media/', file.log_path_file)):
        try:
            os.remove(path=os.path.join('/var/www/html/media/', file.log_path_file))
        except Exception as error:
            print(error)
            file.status("couldn't delete the import")

    if os.path.isdir(os.path.dirname(os.path.join('/var/www/html/media/', file.log_path_file))):
        try:
            shutil.rmtree(os.path.dirname(os.path.join('/var/www/html/media/', file.log_path_file)))
        except Exception as error:
            print(error)
            file.status("couldn't delete the import")

    try:
        file.delete()
    except Exception as error:
        print(error)
        file.status("can't delete the object in database")
    url = build_url('admin/list_of_import_in_database', get={'page': str(page)})
    return HttpResponseRedirect(url)


