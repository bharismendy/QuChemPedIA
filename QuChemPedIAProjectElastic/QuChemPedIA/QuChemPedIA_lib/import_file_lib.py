from QuChemPedIA.models.UserModel import Utilisateur
import os
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import hashlib
import subprocess
import time


def get_base_json():
    """
    function to get the first architecture
    :return: basique json tree
    """
    return '{"job_type": "OPT", "data": {}, "siblings": [],"md5_siblings":[],"contributor":[]}'


def get_siblings_json():
    """
    use to get a sibling json
    :return: json tree of a sibling
    """
    return '{"job_type": "OPT", "data": {}, "siblings": []}'


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


def is_opt_exist(json_to_test, job_type):
    """
    test if there is an opt of the molecule already registered
    :param json_to_test: json of the .log
    :param job_type:
    :return: -1 if it's a new entry else id in elastic search
    """
    solvatation_method = None
    if "OPT" in job_type or "FREQ" in job_type or "TD" in job_type:
        # get value from json
        try:
            inchi = json_to_test['molecule']['inchi']
            cansmiles = json_to_test['molecule']['can']
            smiles = json_to_test['molecule']['smi']
            formula = json_to_test['molecule']['formula']
            software = json_to_test['comp_details']['general']['package']
            theory = json_to_test['comp_details']['general']['all_unique_theory']
            theory = ''.join(map(str, theory))
            functionnal = json_to_test['comp_details']['general']['functional']
            basis_set_md5 = json_to_test['comp_details']['general']['basis_set_md5']
            basis_set_size = json_to_test['comp_details']['general']['basis_set_size']
            charge = json_to_test['molecule']['charge']
            multipicity = json_to_test['molecule']['multiplicity']
            if 'solvent_reaction_field' in json_to_test:
                solvatation_method = json_to_test['comp_details']['general']['solvent_reaction_field']
            solvent = json_to_test['comp_details']['general']['solvent']

        except Exception as error:
            print(error)
            return 4

        try:
            ending_energy = json_to_test['results']['wavefunction']['total_molecular_energy']
            ending_nuclear_repulsion_energy = \
                json_to_test['results']['geometry']['nuclear_repulsion_energy_from_xyz']
        except Exception as error:
            print(error)
            return 4
        try:
            # search a corresponding file in elastic search
            es_host = {"host": "localhost", "port": 9200}
            es = Elasticsearch(hosts=[es_host])
            if solvatation_method is None:
                q = Q('bool',
                      must=[Q('match', data__molecule__inchi=inchi) &
                            Q('match', data__molecule__can=cansmiles) &
                            Q('match', data__molecule__smi=smiles) &
                            Q('match', data__molecule__formula=formula) &
                            Q('match', data__molecule__charge=charge) &
                            Q('match', data__molecule__multiplicity=multipicity) &
                            Q('match', data__comp_details__general__functional=functionnal) &
                            Q('match', data__comp_details__general__package=software) &
                            Q('match', data__comp_details__general__all_unique_theory=theory) &
                            Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                            Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                            Q('match', data__comp_details__general__solvent=solvent) &
                            Q('match', data__results__wavefunction__total_molecular_energy=ending_energy) &
                            Q('match',
                              data__results__geometry__nuclear_repulsion_energy_from_xyz=ending_nuclear_repulsion_energy
                              )
                            ],
                      )
            else:
                q = Q('bool',
                      must=[Q('match', data__molecule__inchi=inchi) &
                            Q('match', data__molecule__can=cansmiles) &
                            Q('match', data__molecule__smi=smiles) &
                            Q('match', data__molecule__formula=formula) &
                            Q('match', data__molecule__charge=charge) &
                            Q('match', data__molecule__multiplicity=multipicity) &
                            Q('match', data__comp_details__general__functionnal=functionnal) &
                            Q('match', data__comp_details__general__package=software) &
                            Q('match', data__comp_details__general__theory=theory) &
                            Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                            Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                            Q('match', data__comp_details__general__solvent=solvent) &
                            Q('match', data__results__wavefunction__total_molecular_energy=ending_energy) &
                            Q('match',
                              data__results__geometry__nuclear_repulsion_energy_from_xyz=ending_nuclear_repulsion_energy
                              )
                            ],
                      )

            s = Search().using(es).query(q)
            s.execute()
            return s
        except Exception as error:
            print(error)
            return 4
    if "SP" in job_type:

        # get value from json
        try:
            inchi = json_to_test['molecule']['inchi']
            cansmiles = json_to_test['molecule']['can']
            smiles = json_to_test['molecule']['smi']
            software = json_to_test['comp_details']['general']['package']
            theory = json_to_test['comp_details']['general']['all_unique_theory']
            theory = ''.join(map(str, theory))
            functionnal = json_to_test['comp_details']['general']['functional']
            basis_set_md5 = json_to_test['comp_details']['general']['basis_set_md5']
            basis_set_size = json_to_test['comp_details']['general']['basis_set_size']
            if 'solvent_reaction_field' in json_to_test:
                solvatation_method = json_to_test['comp_details']['general']['solvent_reaction_field']
            solvent = json_to_test['comp_details']['general']['solvent']
        except Exception as error:
            print(error)
            return 4

        try:
            starting_nuclear_repulsion_energy = json_to_test['molecule']['starting_nuclear_repulsion']
        except Exception as error:
            print(error)
            return 4
        try:
            # search a corresponding file in elastic search
            es_host = {"host": "localhost", "port": 9200}
            es = Elasticsearch(hosts=[es_host])
            if solvatation_method is None:
                q = Q('bool',
                      must=[
                          Q('match', data__molecule__inchi=inchi) &
                          Q('match', data__molecule__can=cansmiles) &
                          Q('match', data__molecule__smi=smiles) &
                          Q('match', data__comp_details__general__functional=functionnal) &
                          Q('match', data__comp_details__general__package=software) &
                          Q('match', data__comp_details__general__all_unique_theory=theory) &
                          Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                          Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                          Q('match', data__comp_details__general__solvent=solvent) &
                          Q('match',
                            data__results__geometry__nuclear_repulsion_energy_from_xyz=starting_nuclear_repulsion_energy
                            )
                            ],
                      )
            else:
                q = Q('bool',
                      must=[
                          Q('match', data__molecule__inchi=inchi) &
                          Q('match', data__molecule__can=cansmiles) &
                          Q('match', data__molecule__smi=smiles) &
                          Q('match', data__comp_details__general__functionnal=functionnal) &
                          Q('match', data__comp_details__general__package=software) &
                          Q('match', data__comp_details__general__theory=theory) &
                          Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                          Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                          Q('match', data__comp_details__general__solvent=solvent) &
                          Q('match',
                            data__results__geometry__nuclear_repulsion_energy_from_xyz=starting_nuclear_repulsion_energy
                            )
                            ],
                      )

            s = Search().using(es).query(q)
            s.execute()
            return s
        except Exception as error:
            print(error)
            return 4


def exist_freq(id_json_to_test, json_to_input, path_to_log_file, destination_dir, id_user):
    """
    test if already exist a freq in a file and if not enter it
    :param id_json_to_test: id of the json to load
    :param json_to_input: json data to input in elastic search
    :param path_to_log_file : path in file system to log file
    :param destination_dir : directory where log are send
    :param id_user: id of the contributor
    :return: True if already entered False if not
    """
    index_name = 'quchempedia_index'
    base_json = get_siblings_json()
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
    path_in_file_sytem = get_path_to_store(destination_dir=destination_dir,
                                           id_calcul=id_json_to_test, make_path=False)
    temp_md5 = json.loads(base_json)
    temp_md5['molecule'] = json_to_input['molecule']
    temp_md5['results'] = json_to_input['results']
    temp_md5['comp_details'] = json_to_input['comp_details']
    temp_md5 = hashlib.md5(str(temp_md5).encode('utf-8')).hexdigest()
    if temp_md5 not in response['_source']['md5_siblings']:
        size = len(response['_source']['siblings'])
        response['_source']['siblings'].append(json.loads(base_json))
        response['_source']['siblings'][size]['data']['molecule'] = json_to_input['molecule']
        response['_source']['siblings'][size]['data']['results'] = json_to_input['results']
        response['_source']['siblings'][size]['data']['comp_details'] = json_to_input['comp_details']
        response['_source']['siblings'][size]['data']['metadata'] = json_to_input['metadata']
        response['_source']['siblings'][size]['data']['metadata']["id_user"] = id_user
        response['_source']['siblings'][size]['data']['metadata']["affiliation"] = get_affiliation(
            id_user=id_user)
        response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
            path_in_file_sytem + "FREQ_" + str(temp_md5) + ".json"
        response['_source']['siblings'][size]['job_type'] = "FREQ"

        response['_source']['md5_siblings'].append(temp_md5)
        response['_source']['contributor'].append(id_user)
        json.dumps(response, indent=4)
        try:
            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
            subprocess.Popen(["mv", path_to_log_file,
                              destination_dir + path_in_file_sytem + "/FREQ_" + str(temp_md5) + ".json"])
                            # copie du JSON
            return 0
        except Exception as error:
            print(error)
            return 4
    else:
        return 1


def exist_td(id_json_to_test, json_to_input, path_to_log_file, destination_dir, id_user):
    """
    test if already exist a td in a file and if not enter it
    :param id_json_to_test: id of the json to load
    :param json_to_input: json data to input in elastic search
    :param path_to_log_file : path in file system to log file
    :param destination_dir : directory where log are send
    :param id_user: id of the contributor
    :return: True if already entered False if not
    """
    index_name = 'quchempedia_index'
    base_json = get_siblings_json()
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
    path_in_file_sytem = get_path_to_store(destination_dir=destination_dir,
                                           id_calcul=id_json_to_test, make_path=False)

    temp_md5 = json.loads(base_json)
    temp_md5['molecule'] = json_to_input['molecule']
    temp_md5['results'] = json_to_input['results']
    temp_md5['comp_details'] = json_to_input['comp_details']
    temp_md5 = hashlib.md5(str(temp_md5).encode('utf-8')).hexdigest()

    if temp_md5 not in response['_source']['md5_siblings']:
        size = len(response['_source']['siblings'])
        response['_source']['siblings'].append(json.loads(base_json))
        response['_source']['siblings'][size]['data']['molecule'] = json_to_input['molecule']
        response['_source']['siblings'][size]['data']['results'] = json_to_input['results']
        response['_source']['siblings'][size]['data']['comp_details'] = json_to_input['comp_details']
        response['_source']['siblings'][size]['data']['metadata'] = json_to_input['metadata']
        response['_source']['siblings'][size]['data']['metadata']["id_user"] = id_user
        response['_source']['siblings'][size]['data']['metadata']["affiliation"] = get_affiliation(
            id_user=id_user)
        response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
            path_in_file_sytem + "TD_" + str(temp_md5) + ".json"
        response['_source']['siblings'][size]['job_type'] = "TD"

        response['_source']['md5_siblings'].append(temp_md5)
        response['_source']['contributor'].append(id_user)
        json.dumps(response, indent=4)
        try:
            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
            path_in_file_sytem = get_path_to_store(destination_dir=destination_dir,
                                                   id_calcul=id_json_to_test, make_path=False)
            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
            subprocess.Popen(["mv", path_to_log_file,
                              destination_dir + path_in_file_sytem + "/TD_" + str(
                                  temp_md5) + ".json"])  # copie du JSON
            return 0
        except Exception as error:
            print(error)
            return 4
    else:
        return 1


def exist_sp(id_json_to_test, json_to_input, path_to_log_file, destination_dir, id_user):
    """
    test if already exist a sp in a file and if not enter it
    :param id_json_to_test: id of the json to load
    :param json_to_input: json data to input in elastic search
    :param path_to_log_file : path in file system to log file
    :param destination_dir : directory where log are send
    :param id_user: id of the contributor
    :return: True if already entered False if not
    """
    index_name = 'quchempedia_index'
    base_json = get_siblings_json()
    es_host = {"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[es_host])
    response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
    path_in_file_sytem = get_path_to_store(destination_dir=destination_dir,
                                           id_calcul=id_json_to_test, make_path=False)
    temp_md5 = json.loads(base_json)
    temp_md5['molecule'] = json_to_input['molecule']
    temp_md5['results'] = json_to_input['results']
    temp_md5['comp_details'] = json_to_input['comp_details']
    temp_md5 = hashlib.md5(str(temp_md5).encode('utf-8')).hexdigest()
    if temp_md5 not in response['_source']['md5_siblings']:
        size = len(response['_source']['siblings'])
        response['_source']['siblings'].append(json.loads(base_json))
        response['_source']['siblings'][size]['data']['molecule'] = json_to_input['molecule']
        response['_source']['siblings'][size]['data']['results'] = json_to_input['results']
        response['_source']['siblings'][size]['data']['comp_details'] = json_to_input['comp_details']
        response['_source']['siblings'][size]['data']['metadata'] = json_to_input['metadata']
        response['_source']['siblings'][size]['data']['metadata']["id_user"] = id_user
        response['_source']['siblings'][size]['data']['metadata']["affiliation"] = get_affiliation(id_user=id_user)
        response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
            path_in_file_sytem + "SP_" + str(temp_md5) + ".json"
        response['_source']['siblings'][size]['job_type'] = "SP"

        response['_source']['md5_siblings'].append(temp_md5)
        response['_source']['contributor'].append(id_user)
        json.dumps(response, indent=4)
        try:
            es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
            path_in_file_sytem = get_path_to_store(destination_dir=destination_dir,
                                                   id_calcul=id_json_to_test, make_path=False)
            subprocess.Popen(["mv", path_to_log_file,
                              destination_dir + path_in_file_sytem + "/SP_" + str(
                                  temp_md5) + ".json"])  # copie du JSON
            return 0
        except Exception as error:
            print(error)
            return 4
    else:
        return 1


def create_query(path, destination_dir, id_user):
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
    es_host = {"host": "localhost", "port": 9200}
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
    jsonfile = open(path)
    if is_json(path=path):
        loaded_json = json.load(jsonfile)
        # set up all OPT
        s = is_opt_exist(json_to_test=loaded_json,
                         job_type=loaded_json['comp_details']['general']['job_type'])
        if not s:
            return 4
        if loaded_json['metadata']['archivable'] == "True" and \
                loaded_json['metadata']['archivable_for_new_entry'] == "True" and \
                "OPT" in loaded_json['comp_details']['general']['job_type'] and s.count() == 0:
            if "FREQ" in loaded_json['comp_details']['general']['job_type']:
                # store data into the json
                temp = json.loads(base_json)
                temp['data']['molecule'] = loaded_json['molecule']
                temp['data']['results'] = loaded_json['results']
                temp['data']['comp_details'] = loaded_json['comp_details']
                temp['data']['metadata'] = loaded_json['metadata']
                temp['data']['metadata']['log_file'] = path
                temp['data']['metadata']["id_user"] = id_user
                temp['data']['metadata']['metadata']["affiliation"] = get_affiliation(
                    id_user=id_user)
                temp['job_type'] = "OPT"
                temp['siblings'].append(json.loads(base_json))
                temp['siblings'][0]['job_type'] = "FREQ"
                temp['md5_siblings'].append(
                    hashlib.md5(str(loaded_json).encode('utf-8')).hexdigest())
                temp['contributor'].append(id_user)

                temp = json.dumps(temp, indent=4)
            else:
                # store data into the json
                temp = json.loads(base_json)
                temp['data']['molecule'] = loaded_json['molecule']
                temp['data']['results'] = loaded_json['results']
                temp['data']['comp_details'] = loaded_json['comp_details']
                temp['data']['metadata'] = loaded_json['metadata']
                temp['data']['metadata']["id_user"] = id_user
                temp['data']['metadata']["affiliation"] = get_affiliation(
                    id_user=id_user)
                temp['data']['metadata']['log_file'] = path
                temp['job_type'] = "OPT"
                temp['contributor'].append(id_user)

                temp = json.dumps(temp, indent=4)
            try:
                response = es.index(index=index_name, doc_type="log_file", body=temp)
                id_file = response['_id']
                path_in_file_system = get_path_to_store(destination_dir=destination_dir,
                                                        id_calcul=id_file, make_path=True)

                response = es.get(index="quchempedia_index", doc_type="log_file", id=id_file)
                response['_source']['data']['metadata']['log_file'] = \
                    path_in_file_system + "OPT_" + str(int(round(time.time() * 1000))) + ".json"
                if "FREQ" in loaded_json['comp_details']['general']['job_type']:
                    response['_source']['siblings'][0]['data']['metadata']['log_file'] = \
                        path_in_file_system + "FREQ_" + str(int(time.time())) + ".json"
                subprocess.Popen(["mv", path, destination_dir + path_in_file_system + "/OPT_" +
                                  str(int(round(time.time() * 1000))) + ".json"])  # copie du JSON
                return 0
            except Exception as error:
                print(error)
                return 4
        elif loaded_json['metadata']['archivable'] == "True" and \
                loaded_json['metadata']['archivable_for_new_entry'] == "True" and \
                "OPT" in loaded_json['comp_details']['general']['job_type'] and s.count() > 0:
            return 1
        elif loaded_json['metadata']['archivable'] == "True":
            if "FREQ" in loaded_json['comp_details']['general']['job_type'] and \
                    loaded_json['metadata']['archivable_for_new_entry'] == "False" and \
                    s.count() == 1:
                for hit in s:
                    try:
                        return exist_freq(id_json_to_test=hit.meta.id,
                                          json_to_input=loaded_json,
                                          path_to_log_file=path,
                                          destination_dir=destination_dir,
                                          id_user=id_user)
                    except Exception as error:
                        print(error)
                        return 4
            elif "FREQ" in loaded_json['comp_details']['general']['job_type'] and \
                    loaded_json['metadata']['archivable_for_new_entry'] == "False" and \
                    s.count() == 0:
                return 3
            if "SP" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                for hit in s:
                    try:
                        return exist_sp(id_json_to_test=hit.meta.id,
                                        json_to_input=loaded_json,
                                        path_to_log_file=path,
                                        destination_dir=destination_dir,
                                        id_user=id_user)
                    except Exception as error:
                        print(error)
                        return 4
            elif "SP" in loaded_json['comp_details']['general']['job_type'] and s.count() == 0:
                return 3
            if "TD" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                for hit in s:
                    try:
                        return exist_td(id_json_to_test=hit.meta.id,
                                        json_to_input=loaded_json,
                                        path_to_log_file=path,
                                        destination_dir=destination_dir,
                                        id_user=id_user)

                    except Exception as error:
                        print(error)
                        return 4
            elif "TD" in loaded_json['comp_details']['general']['job_type'] and s.count() == 0:
                return 3

            if "OPT_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                return 2
            elif "OPT_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 0:
                return 3

            if "FREQ_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                return 2
            elif "FREQ_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 0:
                return 3

        else:
            print("cant load " + path)
            return 4


def import_file(path, id_user):
    """
    main function to import file
    :param path: pth to the file to import
    :param id_user: id to the user
    :return: 0 for all went ok, 1 for already in DB, 2 theory not supported yet,
    3 doesn't have a grount state, 4 other error (see logs)
    """
    # absolute path to the destination directory where we are going to store all the data
    destination_dir = '/home/etudiant/Documents/stage/QuChemPedIAProjectElastic/data_dir/'

    return create_query(path=path, destination_dir=destination_dir, id_user=id_user)
