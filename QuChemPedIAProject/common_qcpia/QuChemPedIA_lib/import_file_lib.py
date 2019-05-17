from user_qcpia.models.UserModel import Utilisateur
import os
import json
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, Range
from common_qcpia.search import _get_job_type
import subprocess
import time

# CONSTANTE
NRE_PRECISION = -2  # power of 10
TME_PRECISION = -6  # power of 10

def trun_n_d(n, d):
    """
    truncate fonction
    :param n: power of ten
    :param d: float to truncate
    :return: truncated float
    """
    d = d*-1
    s = repr(n).split('.')
    if len(s) == 1:
        return int(s[0])
    return float(s[0] + '.' + s[1][:d])


def get_base_json():
    """
    function to get the first architecture
    :return: basique json tree
    """
    return '{"job_type": "OPT", "data": {}, "siblings": []}'


def get_siblings_json(nre, formula, return_search = False):
    """
    use to get a sibling json
    return_search : return directly the search
    :return: json tree of a sibling
    """
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    truncated_nre = trun_n_d(nre, NRE_PRECISION)
    q = Q('bool',
          must=[Q('match', data__molecule__formula=formula)])
    q2 = Q('bool', data__results__nuclear_repulsion_energy_from_xyz=Range(gte=truncated_nre,
                                                                          lt=truncated_nre+10**NRE_PRECISION))

    s = Search(index='quchempedia_index').using(es).query(q).query(q2)
    response = s.execute()
    result = []
    if return_search:
        return response
    else:
        for hit in response:
            try:
                result.append({
                    "id_log": hit.meta.id,
                    "job": _get_job_type(hit)
                })
            except Exception as error:
                print(error)
        return result


def does_file_exist_in_dir(dir_path):
    """
    test if there is file in subdirectory of a folder
    :param dir_path: path to the directory
    :return: boolean answer True = there is file False = no more file
    """
    for files in os.walk(dir_path):
        if files:
            return True
    return False


def is_json(path):
    """
    function to test a file can be load as json
    :param path: path to the file
    :return: boolean answer True = it's a properly formated json, False it's not
    """
    with open(path) as jsonfile:
        try:
            json.load(jsonfile)
        except Exception as error:
            print(error)
            return False
        return True


def get_affiliation(id_user):
    """
    function to get the affiliation of the user
    :param id_user: id of the user
    :return: string that contain the affiliation
    """
    user = Utilisateur.objects.get(id=id_user)
    return user.affiliation.strip()


def clean_file(list_dir, path):
    for element in list_dir:
        if not os.path.isdir(path + '/' + element):
            list_dir.remove(element)
    return list_dir


def get_path_to_store(destination_dir, id_calcul, make_path=False, number_of_subdir=20, cut_number_by=1):
    """
    method to find the right directory to store data
    :param destination_dir: root directory
    :param id_calcul: id of the calcul in database if none (=0) create a new directory
    :param make_path: if set to true, create the directory in file system
    :param number_of_subdir: number of subdirectory in the file system
    :param cut_number_by: the length of the name of each sub dir example 4 = "eeee"/"aaaa"
    :return: path to the destination
    """
    if len(id_calcul) > number_of_subdir:
        print("error in the path for id " + id_calcul)
        exit()
    if len(id_calcul) < number_of_subdir:  # add the subdir
        id_calcul = id_calcul.zfill(number_of_subdir * cut_number_by)

    path_in_file_system = '/'.join(id_calcul[i:i+cut_number_by] for i in range(0, len(id_calcul), cut_number_by))
    if make_path:
        try:
            os.makedirs(destination_dir + path_in_file_system)
        except Exception as error:
            print(error)
            return 4

    return path_in_file_system


def update_siblings(list_of_siblings, id_file, job_type):
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    index_name = 'quchempedia_index'
    print(list_of_siblings[0])
    for sib in list_of_siblings:
        response = es.get(index=index_name, doc_type="log_file", id=sib["id_log"])
        temp_sib = response['_source']['siblings']
        temp_sib.append({"id_log": id_file, "job": job_type})
        response['_source']['siblings'] = temp_sib
        es.index(index=index_name, doc_type="log_file", body=response['_source'], id=sib["id_log"])

        
def update_submission(last_sub, id_user, id_file, new_ref=False):
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    index_name = 'quchempedia_index'

    temp = es.get(index=index_name, doc_type="log_file", id=last_sub)
    list_of_sub = temp['_source']['data']['metadata']['submissions']
    if new_ref:
        temp['_source']['data']['metadata']['ref_sub'] = id_file
    if not len(list_of_sub) > 0:
        temp_sub = temp['_source']['data']['metadata']['submissions']
        temp_sub.append({"id_log": id_file, "author": id_user})
        if new_ref:
            temp['_source']['data']['metadata']['ref_sub'] = id_file
        temp['_source']['data']['metadata']['submissions'] = temp_sub
        es.index(index=index_name, doc_type="log_file", body=temp['_source'], id=last_sub)

    else:
        for sub in list_of_sub:
            response = es.get(index=index_name, doc_type="log_file", id=sub["id_log"])
            temp_sub = response['_source']['data']['metadata']['submissions']
            temp_sub.append({"id_log": id_file, "author": id_user})
            response['_source']['siblings'] = temp_sub
            if new_ref:
                response['_source']['data']['metadata']['ref_sub'] = id_file

            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=sub["id_log"])


def create_query_log(path, json_file, destination_dir, id_user):
    """
       this function get all file from the source directory to store them in the destination directory
       we put the log in database and the json in elasticSearch
       :param path: directory or file path that contains the new .log
       :param destination_dir: the directory where we are going to store our .log
       :param id_user: id of the contributor
       :return: nothing
       """
    # iterate on all file
    # setting conection to elastic search server
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    base_json = get_base_json()
    # creating the index
    index_name = 'quchempedia_index'
    if not es.indices.exists(index=index_name):
        try:
            response = es.indices.create(index=index_name)
            print(response)
        except Exception as error:
            print(error)
            return 4
    loaded_json = json_file

    if loaded_json['metadata']['archivable'] == "True" and loaded_json['metadata']['archivable_for_new_entry'] == "True":
        # we get the siblings to test how many they are
        siblings = None
        nre = loaded_json['results']['geometry']['nuclear_repulsion_energy_from_xyz']
        formula = loaded_json['molecule']['formula']
        solveur = loaded_json['comp_details']['general']['package']
        tme = loaded_json['results']['wavefunction']['total_molecular_energy']  # total molecular energy
        job_type = _get_job_type(json_file)
        author = id_user
        try:
            siblings = get_siblings_json(nre=nre,
                                         formula=formula,
                                         return_search=True)
        except Exception as error:
            print(error)

        #  boolean to know if it's a sibling or a submission
        new_sib = False
        new_sub = False
        new_ref = False
        ref_prec_sub = None
        if siblings.hits.total > 0:
            for hit in siblings:
                if hit.job_type[0] in job_type:
                    if hit.data.comp_details.general.package == solveur:
                        truncated_tme = trun_n_d(hit.data.results.wavefunction.total_molecular_energy, TME_PRECISION)

                        if truncated_tme <= tme < truncated_tme+10**NRE_PRECISION:
                            if hit.data.metadata.id_user == author:
                                return 3
                            try:
                                if hit.data.metadata.discretizable:
                                    new_ref = True
                                    break
                                else:
                                    return 3
                            except:
                                pass
                        else:
                            new_sub = True
                            ref_prec_sub = hit.meta.id
                            break
                    else:
                        new_sub = True
                        ref_prec_sub = hit.meta.id
                        break
                else:
                    new_sib = True
                    break

        # store data into the json
        siblings = get_siblings_json(nre=nre,
                                     formula=formula)
        temp = json.loads(base_json)
        temp['data']['molecule'] = loaded_json['molecule']
        temp['data']['results'] = loaded_json['results']
        temp['data']['comp_details'] = loaded_json['comp_details']
        temp['data']['metadata'] = loaded_json['metadata']
        temp['data']['metadata']['log_file'] = path
        temp['data']['metadata']["id_user"] = id_user
        temp['data']['metadata']['submissions'] = []
        if new_sib:
            temp['siblings'] = siblings

        temp['data']['metadata']["affiliation"] = get_affiliation(id_user=id_user)
        temp['job_type'] = loaded_json['comp_details']['general']['job_type']
        temp = json.dumps(temp, indent=4)

        try:
            response = es.index(index=index_name, doc_type="log_file", body=temp)
            id_file = response['_id']
            response = es.get(index=index_name, doc_type="log_file", id=id_file)

            if new_sib:
                update_siblings(siblings, id_file, job_type)

            if new_sub:
                response_last_sub = es.get(index=index_name, doc_type="log_file", id=ref_prec_sub)
                if new_ref:
                    update_submission(last_sub=ref_prec_sub, new_ref=new_ref, id_file=id_file, id_user=id_user)
                else:
                    update_submission(last_sub=ref_prec_sub, new_ref=new_ref, id_file=id_file, id_user=id_user)
                current_sub = response_last_sub['_source']['data']['metadata']['submissions']
                current_sub.append({"id_log": id_file, "author": id_user})
                response['_source']['data']['metadata']['submissions'] = current_sub

            else:
                response['_source']['data']['metadata']['submissions'] = [{"id_log": id_file, "author": id_user}]
            path_in_file_system = get_path_to_store(destination_dir=destination_dir,
                                                    id_calcul=id_file, make_path=True)
            location_opt = os.path.join(path_in_file_system + "/"+loaded_json['comp_details']['general']['job_type'][0]+"_" +
                                        str(int(round(time.time() * 1000))) + ".log")
            response['_source']['data']['metadata']['log_file'] = location_opt

            subprocess.Popen(["cp", path, os.path.join(destination_dir + path_in_file_system + "/"+
                                                       loaded_json['comp_details']['general']['job_type'][0]+"_" +
                                                       str(int(round(time.time() * 1000))) + ".log")])  # copie du JSON
            subprocess.Popen(["rm", path])
            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_file)
            return 0
        except Exception as error:
            print(error)
            return 4
    else:
        return 1


def import_file(path, json_file, id_user):
    """
    main function to import file
    :param path: pth to the file to import
    :param id_user: id to the user
    :return: 0 for all went ok, 1 for already in DB, 2 calculatiion not supported yet,
    3 doesn't have a grount state, 4 other error (see logs)
    """
    # absolute path to the destination directory where we are going to store all the data
    destination_dir = settings.DATA_DIR_ROOT+'/'
    es_host = settings.ELASTICSEARCH
    es = Elasticsearch(hosts=[es_host])
    base_json = get_base_json()
    # creating the index
    index_name = 'quchempedia_index'
    if not es.indices.exists(index=index_name):
        try:
            response = es.indices.create(index=index_name)
            print(response)
        except Exception as error:
            print(error)
            return 4
    return create_query_log(path=path, json_file=json_file, destination_dir=destination_dir, id_user=id_user)
