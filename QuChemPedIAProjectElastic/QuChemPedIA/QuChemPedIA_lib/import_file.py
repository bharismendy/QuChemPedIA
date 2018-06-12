from builtins import print

from django.contrib.admin.templatetags.admin_list import results
from django.core.management.base import BaseCommand
import os
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import hashlib
import subprocess
import time


class Command(BaseCommand):

    @staticmethod
    def get_base_json():
        return '{"job_type": "OPT", "data": {}, "siblings": [],"md5_siblings":[]}'

    @staticmethod
    def get_siblings_json():
        return '{"job_type": "OPT", "data": {}, "siblings": []}'

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def clean_file(list_dir, path):
        for element in list_dir:
            if not os.path.isdir(path + '/' + element):
                list_dir.remove(element)
        return list_dir

    @staticmethod
    def is_last(list_dir):
        if len(list_dir) == 0:  # test si on est arrivé au dernier dossier
            return True
        return False

    @staticmethod
    def get_path_to_store(self, destination_dir, id_calcul, make_path=False):
        """
        method to find the right directory to store data
        :param destination_dir: root directory
        :param id_calcul: id of the calcul in database if none (=0) create a new directory
        :param if set to true, create the directory in file system
        :return:
        """
        number_of_subdir = 20
        path_in_file_system = ''
        cut_number_by = 1

        if len(id_calcul) > number_of_subdir:
            print("error in the path for id " + id_calcul)
            exit()
        if len(id_calcul) < number_of_subdir:  # add the subdir
            id_calcul = id_calcul.zfill(number_of_subdir * cut_number_by)

        for elemnent in id_calcul:
            path_in_file_system += str(elemnent) + '/'
        if make_path:
            try:
                os.makedirs(destination_dir + path_in_file_system)
            except Exception as error:
                print(error)

        return path_in_file_system

    @staticmethod
    def is_opt_exist(json_to_test, job_type):
        """
        test if there is an opt of the molecule already registered
        :param json_to_test: json of the .log
        :param job_type:
        :return: -1 if it's a new entry else id in elastic search
        """
        inchi = None
        cansmiles = None
        smiles = None
        formula = None
        software = None
        theory = None
        functionnal = None
        basis_set_md5 = None
        basis_set_size = None
        charge = None
        multipicity = None
        solvatation_method = None
        solvent = None
        ending_energy = None
        ending_nuclear_repulsion_energy = None
        starting_nuclear_repulsion_energy = None
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

            try:
                ending_energy = json_to_test['results']['wavefunction']['total_molecular_energy']
                ending_nuclear_repulsion_energy = \
                    json_to_test['results']['geometry']['nuclear_repulsion_energy_from_xyz']
            except Exception as error:
                print(error)
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
                                  data__results__geometry__nuclear_repulsion_energy_from_xyz=ending_nuclear_repulsion_energy)],
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
                                  data__results__geometry__nuclear_repulsion_energy_from_xyz=ending_nuclear_repulsion_energy)],
                          )

                s = Search().using(es).query(q)
                s.execute()
                return s
            except Exception as error:
                print(error)
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

            try:
                starting_nuclear_repulsion_energy = json_to_test['molecule']['starting_nuclear_repulsion']
            except Exception as error:
                print(error)
            try:
                # search a corresponding file in elastic search
                es_host = {"host": "localhost", "port": 9200}
                es = Elasticsearch(hosts=[es_host])
                if solvatation_method is None:
                    q = Q('bool',
                          must=[Q('match', data__molecule__inchi=inchi) &
                                Q('match', data__molecule__can=cansmiles) &
                                Q('match', data__molecule__smi=smiles) &
                                Q('match', data__comp_details__general__functional=functionnal) &
                                Q('match', data__comp_details__general__package=software) &
                                Q('match', data__comp_details__general__all_unique_theory=theory) &
                                Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                                Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                                Q('match', data__comp_details__general__solvent=solvent) &
                                Q('match',
                                  data__results__geometry__nuclear_repulsion_energy_from_xyz=
                                  starting_nuclear_repulsion_energy)],
                          )
                else:
                    q = Q('bool',
                          must=[Q('match', data__molecule__inchi=inchi) &
                                Q('match', data__molecule__can=cansmiles) &
                                Q('match', data__molecule__smi=smiles) &
                                Q('match', data__comp_details__general__functionnal=functionnal) &
                                Q('match', data__comp_details__general__package=software) &
                                Q('match', data__comp_details__general__theory=theory) &
                                Q('match', data__comp_details__general__basis_set_size=basis_set_size) &
                                Q('match', data__comp_details__general__basis_set_md5__keyword=basis_set_md5) &
                                Q('match', data__comp_details__general__solvent=solvent) &
                                Q('match',
                                  data__results__geometry__nuclear_repulsion_energy_from_xyz=
                                  starting_nuclear_repulsion_energy)],
                          )

                s = Search().using(es).query(q)
                s.execute()
                return s
            except Exception as error:
                print(error)

    def exist_freq(self, id_json_to_test, json_to_input, path_to_log_file, destination_dir):
        """
        test if already exist a freq in a file and if not enter it
        :param id_json_to_test: id of the json to load
        :param json_to_input: json data to input in elastic search
        :param path_to_log_file : path in file system to log file
        :param destination_dir : directory where log are send
        :return: True if already entered False if not
        """
        index_name = 'quchempedia_index'
        base_json = self.get_siblings_json()
        es_host = {"host": "localhost", "port": 9200}
        es = Elasticsearch(hosts=[es_host])
        response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
        path_in_file_sytem = self.get_path_to_store(self, destination_dir=destination_dir,
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
            response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
                path_in_file_sytem + "FREQ_" + str(temp_md5) + ".json"
            response['_source']['siblings'][size]['job_type'] = "FREQ"

            response['_source']['md5_siblings'].append(temp_md5)
            json.dumps(response, indent=4)
            try:
                es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
                subprocess.Popen(["mv", path_to_log_file,
                                  destination_dir + path_in_file_sytem + "FREQ_" + str(
                                      temp_md5) + ".json"])  # copie du JSON
            except Exception as error:
                print(error)

    def exist_td(self, id_json_to_test, json_to_input, path_to_log_file, destination_dir):
        """
        test if already exist a td in a file and if not enter it
        :param id_json_to_test: id of the json to load
        :param json_to_input: json data to input in elastic search
        :param path_to_log_file : path in file system to log file
        :param destination_dir : directory where log are send
        :return: True if already entered False if not
        """
        # TODO factorisation
        index_name = 'quchempedia_index'
        base_json = self.get_siblings_json()
        es_host = {"host": "localhost", "port": 9200}
        es = Elasticsearch(hosts=[es_host])
        response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
        path_in_file_sytem = self.get_path_to_store(self, destination_dir=destination_dir,
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
            response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
                path_in_file_sytem + "TD_" + str(temp_md5) + ".json"
            response['_source']['siblings'][size]['job_type'] = "TD"

            response['_source']['md5_siblings'].append(temp_md5)
            json.dumps(response, indent=4)
            try:
                es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
                path_in_file_sytem = self.get_path_to_store(self, destination_dir=destination_dir,
                                                            id_calcul=id_json_to_test, make_path=False)
                es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
                subprocess.Popen(["mv", path_to_log_file,
                                  destination_dir + path_in_file_sytem + "TD_" + str(
                                      temp_md5) + ".json"])  # copie du JSON
            except Exception as error:
                print(error)

    def exist_sp(self, id_json_to_test, json_to_input, path_to_log_file, destination_dir):
        """
        test if already exist a sp in a file and if not enter it
        :param id_json_to_test: id of the json to load
        :param json_to_input: json data to input in elastic search
        :param path_to_log_file : path in file system to log file
        :param destination_dir : directory where log are send
        :return: True if already entered False if not
        """
        # TODO factorisation
        index_name = 'quchempedia_index'
        base_json = self.get_siblings_json()
        es_host = {"host": "localhost", "port": 9200}
        es = Elasticsearch(hosts=[es_host])
        response = es.get(index="quchempedia_index", doc_type="log_file", id=id_json_to_test)
        path_in_file_sytem = self.get_path_to_store(self, destination_dir=destination_dir,
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
            response['_source']['siblings'][size]['data']['metadata']['log_file'] = \
                path_in_file_sytem + "SP_" + str(temp_md5) + ".json"
            response['_source']['siblings'][size]['job_type'] = "SP"

            response['_source']['md5_siblings'].append(temp_md5)
            json.dumps(response, indent=4)
            try:
                es.index(index=index_name, doc_type="log_file", body=response['_source'], id=id_json_to_test)
                path_in_file_sytem = self.get_path_to_store(self, destination_dir=destination_dir,
                                                            id_calcul=id_json_to_test, make_path=False)
                subprocess.Popen(["mv", path_to_log_file,
                                  destination_dir + path_in_file_sytem + "SP_" + str(
                                      temp_md5) + ".json"])  # copie du JSON
            except Exception as error:
                print(error)

    def _create_query(self, path, destination_dir):

        # todo remplacer log_file par le chemin vers le fichiers dans le système
        # todo tester sans donner d'ordre
        """
        this function get all file from the source directory to store them in the destination directory
        we put the log in database and the json in elasticSearch
        :param source_dir: directory or file path that contains the new .log
        :param destination_dir: the directory where we are going to store our .log
        :return: nothing
        """

        # iterate on all file
        # setting conection to elastic search server
        es_host = {"host": "localhost", "port": 9200}
        es = Elasticsearch(hosts=[es_host])
        base_json = self.get_base_json()
        # creating the index
        index_name = 'quchempedia_index'
        if not es.indices.exists(index=index_name):
            try:
                response = es.indices.create(index=index_name)
                print(response)
            except Exception as error:
                print(error)
        jsonfile = open(path)
        if self.is_json(path=path):
            loaded_json = json.load(jsonfile)
            # set up all OPT
            s = self.is_opt_exist(json_to_test=loaded_json,
                                  job_type=loaded_json['comp_details']['general']['job_type'])
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
                    temp['job_type'] = "OPT"
                    temp['siblings'].append(json.loads(base_json))
                    temp['siblings'][0]['job_type'] = "FREQ"
                    temp['md5_siblings'].append(
                        hashlib.md5(str(loaded_json).encode('utf-8')).hexdigest())
                    temp = json.dumps(temp, indent=4)
                else:
                    # store data into the json
                    temp = json.loads(base_json)
                    temp['data']['molecule'] = loaded_json['molecule']
                    temp['data']['results'] = loaded_json['results']
                    temp['data']['comp_details'] = loaded_json['comp_details']
                    temp['data']['metadata'] = loaded_json['metadata']
                    temp['job_type'] = "OPT"
                    temp = json.dumps(temp, indent=4)
                try:
                    response = es.index(index=index_name, doc_type="log_file", body=temp)
                    id = response['_id']
                    path_in_file_system = self.get_path_to_store(self, destination_dir=destination_dir,
                                                                 id_calcul=id, make_path=True)

                    response = es.get(index="quchempedia_index", doc_type="log_file", id=id)
                    response['_source']['data']['metadata']['log_file'] = \
                        path_in_file_system + "OPT_" + str(int(round(time.time() * 1000))) + ".json"

                    if "FREQ" in loaded_json['comp_details']['general']['job_type']:
                        response['_source']['siblings'][0]['data']['metadata']['log_file'] = \
                            path_in_file_system + "FREQ_" + str(int(time.time())) + ".json"
                    subprocess.Popen(["mv", path, destination_dir + path_in_file_system + "OPT_" +
                                      str(int(round(time.time() * 1000))) + ".json"])  # copie du JSON
                    get_valid_file = True

                except Exception as error:
                    print(error)
                    get_valid_file = False

            if loaded_json['metadata']['archivable'] == "True":
                if "FREQ" in loaded_json['comp_details']['general']['job_type'] and \
                        loaded_json['metadata']['archivable_for_new_entry'] == "False" and \
                        s.count() == 1:
                    for hit in s:
                        try:
                            self.exist_freq(id_json_to_test=hit.meta.id,
                                            json_to_input=loaded_json,
                                            path_to_log_file=path,
                                            destination_dir=destination_dir)
                            get_valid_file = True
                        except Exception as error:
                            print(error)
                            get_valid_file = False

                if "SP" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                    for hit in s:
                        try:
                            self.exist_sp(id_json_to_test=hit.meta.id,
                                          json_to_input=loaded_json,
                                          path_to_log_file=path,
                                          destination_dir=destination_dir)
                            get_valid_file = True
                        except Exception as error:
                            print(error)
                            get_valid_file = False

                if "TD" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                    for hit in s:
                        try:
                            self.exist_td(id_json_to_test=hit.meta.id,
                                          json_to_input=loaded_json,
                                          path_to_log_file=path,
                                          destination_dir=destination_dir)
                            get_valid_file = True
                        except Exception as error:
                            print(error)
                            get_valid_file = False

                """
                if "OPT_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                    pass
                if "FREQ_ES" in loaded_json['comp_details']['general']['job_type'] and s.count() == 1:
                    pass
                """

            else:
                print("cant load "+ path)
                os.remove(path)

    def import_file(self, path, destination_dir):
        # absolute path to the source directory where are all the data
        source_dir = path

        # absolute path to the destination directory where we are going to store all the data
        destination_dir = '/home/etudiant/Documents/stage/QuChemPedIAProjectElastic/data_dir/'

        self._create_query(path=source_dir, destination_dir=destination_dir)