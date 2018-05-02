from builtins import print
from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import os
import json
import csv
import subprocess
from datetime import datetime
from QuChemPedIA.models.UserModel import utilisateur
from QuChemPedIA.models.JobTypeModel import JobType
from QuChemPedIA.models.FunctionnalModel import functionnal
from QuChemPedIA.models.TheoryModel import theory
from QuChemPedIA.models.SoftwareModel import software
"""
    Utilisation de cette commande :
                            -activer le virtualenv (source venv/bin/activate
                            -mettez à jour le destination_dir et le source dir
                            -mettez à jour la base de donnée avec les commandes suivantes :
                                -python manage.py makemigrations QuChemPedIA
                                -python manage.py migrate
                            -déplacez vous dans le dossier QuChemPedIAProject 
                            -entrer dans le terminal la commande : python manage.py populate_db
"""


class Command(BaseCommand):
    def is_json(self, path):
        with open(path) as jsonfile:
            try:
                json_object = json.load(jsonfile)
            except Exception as error:
                print(error)
                return False
            return True

    def clean_file(self, list_dir, path):
        for element in list_dir:
            if not os.path.isdir(path+'/'+element):
                list_dir.remove(element)
        return list_dir

    def is_last(self, list_dir):
        if len(list_dir) == 0:  # test si on est arrivé au dernier dossier
            return True
        return False

    def store(self, destination_dir):
        for dirpath, dirs, files in os.walk(destination_dir):
            if len(dirs) < 25000:
                list_dir = os.listdir(dirpath)
                list_dir = self.clean_file(list_dir, dirpath)
                if self.is_last(list_dir):
                    path = dirpath+'/..'
                    list_dir = os.listdir(path)
                    list_dir = self.clean_file(list_dir, path)
                    list_dir.sort(key=int)
                    while not len(list_dir) < 25000:
                        path = path + '/..'
                        if destination_dir in path:
                            list_dir = os.listdir(path)
                            list_dir = self.clean_file(list_dir, path)
                            list_dir.sort(key=int)
                        else:
                            print("ERROR FILE SYSTEM IS FULL")
                        print(path)
                    # on créer le répertoire et on met le calcul
                    name_dir = list_dir[len(list_dir)-1]
                    name_dir = int(name_dir)+1
                    name_dir = path+'/'+str(name_dir)
                    subprocess.Popen(["mkdir", name_dir])
                    return name_dir+'/'

    def _create_query(self, source_dir, destination_dir, relation_file):
        # iterate on all file
        for dir in os.listdir(source_dir):
            for filename in os.listdir(source_dir+'/'+dir):
                if '.json' in filename:
                    path = source_dir+'/'+dir+'/'+filename
                    temp = Query()
                    user = utilisateur.objects
                    job = JobType.objects
                    # TODO must be validate
                    theorie = theory.objects
                    soft = software.objects
                    funct = functionnal.objects
                    jsonfile = open(path)
                    if self.is_json(path):
                        loaded_json = json.load(jsonfile)
                        # getting data for jobtype object
                        # try to get the name
                        try:
                            name = "testing"
                        except Exception as error:
                            print("error for getting the name of the job_type : ")
                            print(error)

                        # try to register the job_type
                        try:
                            # we check if it's already exist, if not we register it
                            job, created= JobType.objects.update_or_create(name=name)
                        except Exception as error:
                            print("error for registering the job_type : ")
                            print(error)

                        # getting data for user object
                        # try to get the name
                        try:
                            name = loaded_json['authorship']['primary_author'].strip()
                        except Exception as error:
                            print("error for getting the primary author : ")
                            print(error)

                        # try to get the orcid
                        try:
                            orcid = loaded_json['authorship']['primary_author_orcid'].strip()
                        except Exception as error:
                            print("error for getting the orcid : ")
                            print(error)

                        # try to get the affiliation
                        try:
                            affiliation = loaded_json['authorship']['primary_author_affiliation'].strip()
                        except Exception as error:
                            print("error for getting the affiliation : ")
                            print(error)

                        # try to register the user
                        try:
                            # we check if it's already exist, if not we register it
                            user, created= utilisateur.objects.update_or_create(name=name, orcid=orcid, affiliation=affiliation)

                        except Exception as error:
                            print("error for registering the user : ")
                            print(error)

                        # getting for query object
                        # try to get the inchi
                        try:
                            temp.inchi = loaded_json['molecule']['inchi'][0].strip()
                        except Exception as error :
                            print("error for getting the InChi : ")
                            print(error)

                        # try to get the formula
                        try:
                            temp.formula = loaded_json['molecule']['formula'].strip()
                        except Exception as error:
                            print("error for getting the formula : ")
                            print(error)

                        # try to get the SMILES
                        try:
                            temp.smiles = loaded_json['molecule']['smi'].strip()
                        except Exception as error:
                            print("error for getting the SMILES : ")
                            print(error)

                        # try to get the theory
                        try:
                            nameTheorie = loaded_json['comp_details']['general']['all_unique_theory'][0].strip()
                        except Exception as error:
                            print("error for getting the theory :")
                            print(error)

                        # try to register the theory
                        try:
                            # we check if it's already exist, if not we register it
                            theorie, created= theory.objects.update_or_create(name=nameTheorie)
                        except Exception as error:
                            print("error for registering the theory : ")
                            print(error)

                        # try to get the functionnal
                        try:
                            nameFunctionnal = loaded_json['comp_details']['general']['functional'].strip()
                        except Exception as error:
                            print("error for getting the ending_energy : ")
                            print(error)

                        # try to register the functionnal
                        try:
                            # we check if it's already exist, if not we register it
                            funct, created= functionnal.objects.update_or_create(name=nameFunctionnal)
                        except Exception as error:
                            print("error for registering the functionnal : ")
                            print(error)

                        # try to get the software
                        try:
                            nameSoftware = loaded_json['comp_details']['general']['package'].strip()
                        except Exception as error:
                            print("error for getting the software : ")
                            print(error)

                        # try to register the software
                        try:
                            # we check if it's already exist, if not we register it
                            soft, created= software.objects.update_or_create(name=nameSoftware)
                        except Exception as error:
                            print("error for registering the software : ")
                            print(error)

                        # try to get the starting_nuclear_repulsion_energy
                        try:
                            temp.starting_nuclear_repulsion_energy = loaded_json['molecule']['starting_nuclear_repulsion']
                        except Exception as error:
                            print("error for getting the starting_nuclear_repulsion_energy : ")
                            print(error)

                        # try to get the ending_nuclear_repulsion_energy
                        try:
                            temp.ending_nuclear_repulsion_energy = loaded_json['results']['geometry']['nuclear_repulsion_energy_from_xyz']
                        except Exception as error:
                            print("error for getting the ending_nuclear_repulsion_energy : ")
                            print(error)

                        # try to get the charge
                        try:
                            temp.charge = loaded_json['molecule']['charge']
                        except Exception as error:
                            print("error for getting the charge : ")
                            print(error)

                        # try to get the cansmiles
                        try:
                            temp.cansmiles = loaded_json['molecule']['can'].strip()
                        except Exception as error:
                            print("error for getting the cansmiles : ")
                            print(error)

                        # try to get the multiplicity
                        try:
                            temp.multiplicity = loaded_json['molecule']['multiplicity']
                        except Exception as error:
                            print("error for getting the multiplicity : ")
                            print(error)

                        # try to get the basis_set_name
                        try:
                            temp.basis_set_name = loaded_json['comp_details']['general']['basis_set_name'].strip()
                        except Exception as error:
                            print("error for getting the basis_set_name : ")
                            print(error)

                        # try to get the basis_set_size
                        try:
                            temp.basis_set_size = loaded_json['comp_details']['general']['basis_set_size']
                        except Exception as error:
                            print("error for getting the basis_set_size : ")
                            print(error)

                        # try to get the solvent_method
                        try:
                            temp.solvent_method = loaded_json['comp_details']['general']['solvent_reaction_field'].strip()
                        except Exception as error:
                            print("error for getting the solvent_method :")
                            print(error)

                        # try to get the solvent
                        try:
                            temp.solvent = loaded_json['comp_details']['general']['solvent'].strip()
                        except Exception as error:
                            print("error for getting the solvent :")
                            print(error)

                        # try to get the starting_energy
                        try:
                            temp.starting_energy = loaded_json['molecule']['starting_energy']
                        except Exception as error:
                            print("error for getting the starting_energy :")
                            print(error)

                        # try to get the ending_energy
                        try:
                            temp.ending_energy = loaded_json["results"]["wavefunction"]["total_molecular_energy"]
                        except Exception as error:
                            print("error for getting the ending_energy :")
                            print(error)

                        # try to get the HOMO
                        try:
                            index = loaded_json['results']['wavefunction']['homo_indexes']
                            if len(index) == 2:
                                if -1 not in index:
                                    index_0 = index[0]
                                    temp.homo_alpha_energy = loaded_json["results"]["wavefunction"]["MO_energies"][0][index_0]
                                    index_1 = index[1]
                                    temp.homo_beta_energy = loaded_json["results"]["wavefunction"]["MO_energies"][1][index_1]
                                else:
                                    index_0 = index[0]
                                    temp.homo_alpha_energy = loaded_json["results"]["wavefunction"]["MO_energies"][0][index_0]
                            if len(index) == 1:
                                index_0 = index[0]
                                temp.homo_alpha_energy = loaded_json["results"]["wavefunction"]["MO_energies"][0][index_0]
                        except Exception as error:
                            print("error for getting the HOMO :")
                            print(error)

                        # try to get the Lumo
                        try:
                            index = loaded_json["results"]["wavefunction"]["homo_indexes"]
                            if len(index) == 2:
                                index_0 = index[0]
                                if not index == -1:
                                    temp.homo_alpha_energy = loaded_json["results"]["wavefunction"]["MO_energies"][0][index_0-1]
                                index_1 = index[1]
                                if not index == -1:
                                    temp.homo_beta_energy = loaded_json["results"]["wavefunction"]["MO_energies"][1][index_1-1]
                        except Exception as error:
                            print("error for getting the LUMO : ")
                            print(error)

                        # getting the CID and the IUPAC
                        try:
                            formule = loaded_json['molecule']['formula'].strip()
                            # open the csv
                            csv_file = open(relation_file, 'r')
                            reader = csv.reader(csv_file, delimiter=";")
                            for rows in reader:
                                if formule == rows[1].strip():
                                    temp.cid = rows[0].strip()
                                    temp.iupac = rows[2].strip()  # we make a strip to escape all whitespace
                                    break
                            csv_file.close()
                        except Exception as error:
                            print("error for getting the IUPAC/CID : ")
                            print(error)

                        # store the file in data bank
                        # temp.files_path = self.store(destination_dir)
                        # subprocess.Popen(["cp", path, temp.files_path])#copie du JSON
                        # TODO copie du pdf+jpeg
                        temp.files_path = path
                        temp.date = datetime.now()
                        temp.job_type = job
                        temp.user = user
                        temp.theory = theorie
                        temp.functional = funct
                        temp.software = soft
                        try:
                            temp.save()
                        except Exception as error:
                            print("error can't write this compute sheet :")
                            print(error)
                            print(temp.files_path)

                    else:
                        print("cant load " + source_dir+'/'+dir+'/'+filename)

    def handle(self, *args, **options):
        # absolute path to the source directory where are all the data
        source_dir = '/home/etudiant/Documents/stage/data_brice/fchk_log_files'

        # absolute path to the destination directory where we are going to store all the data
        destination_dir = '/home/etudiant/Documents/stage/data_dir/'

        # absolute path to the reation file
        relation_file = '/home/etudiant/Documents/stage/data_brice/names50k.csv'
        self._create_query(source_dir=source_dir, destination_dir=destination_dir, relation_file=relation_file)
