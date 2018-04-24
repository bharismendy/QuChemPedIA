from builtins import print

from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import os
import json
import csv
import subprocess
from datetime import datetime
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
    def is_json(self,path):
        with open(path) as jsonfile:
            try:
                json_object = json.load(jsonfile)
            except :
                return False
            return True

    def cleanFile(self, listDir,path):
        for element in listDir:
            if not os.path.isdir(path+'/'+element):
                listDir.remove(element)
        return listDir

    def isLast(self,list_dir):
        if len(list_dir) == 0:  # test si on est arrivé au dernier dossier
            return True
        return False

    def store(self, destination_dir):
        for dirpath, dirs, files in os.walk(destination_dir):
            if len(dirs)<25000 :
                list_dir = os.listdir(dirpath)
                list_dir = self.cleanFile(list_dir,dirpath)
                if self.isLast(list_dir):
                    path = dirpath+'/..'
                    list_dir = os.listdir(path)
                    list_dir = self.cleanFile(list_dir,path)
                    list_dir.sort(key=int)
                    while not len(list_dir)<25000:
                        path = path + '/..'
                        if destination_dir in path :
                            list_dir = os.listdir(path)
                            list_dir = self.cleanFile(list_dir, path)
                            list_dir.sort(key=int)
                        else :
                            print("ERROR FILE SYSTEM IS FULL")
                        print(path)
                    # on créer le répertoire et on met le calcul
                    name_dir = list_dir[len(list_dir)-1]
                    name_dir =int(name_dir)+1
                    name_dir = path+'/'+str(name_dir)
                    subprocess.Popen(["mkdir", name_dir])
                    return name_dir+'/'

    def _create_query(self,source_dir,destination_dir,relation_file):
        # iterate on all file
        for dir in os.listdir(source_dir) :
            for filename in os.listdir(source_dir+'/'+dir):
                if '.json' in filename:
                    path = source_dir+'/'+dir+'/'+filename
                    temp = Query()
                    jsonfile = open(path)
                    if self.is_json(path):
                        loaded_json = json.load(jsonfile)

                        # try to get the inchi
                        try:
                            temp.inchi = loaded_json['molecule']['inchi'][0]
                        except:
                            temp.inchi = None

                        # try to get the formula
                        try:
                            temp.formula =loaded_json['molecule']['formula']
                        except:
                            temp.formula = None

                        # try to get the SMILES
                        try:
                            temp.smiles = loaded_json['molecule']['smi']
                        except:
                            temp.smiles = None

                        # try to get the theory
                        try:
                            temp.theory = loaded_json['comp_details']['general']['all_unique_theory'][0]
                        except:
                            temp.theory = None

                        # try to get the functionnal
                        try:
                            temp.functional = loaded_json['comp_details']['general']['functional']
                        except:
                            temp.functional = None

                        # try to get the software
                        try:
                            temp.software = loaded_json['comp_details']['general']['package']
                        except:
                            temp.software = None

                        # try to get the nuclear starting energy
                        try:
                            val = loaded_json['comp_details']['molecule']['starting_energy']
                            if not val in "N/A":
                                temp.nuclear_starting_energy = val
                        except:
                            temp.nuclear_starting_energy = None

                        # try to get the nuclear ending energy
                        try:
                            val = loaded_json['results']['geometry']['geometric_values']['nuclear_repulsion_energy_from_xyz']
                            if not val in "N/A":
                                temp.nuclear_ending_energy = val
                        except:
                            temp.nuclear_ending_energy = None

                        # try to get the charge
                        try:
                            val = loaded_json['molecule']['charge']
                            if not val in "N/A":
                                temp.charge = val
                        except:
                            temp.charge = None

                        # try to get the cansmiles
                        try:
                            temp.cansmiles = loaded_json['molecule']['can']
                        except:
                            temp.cansmiles = None

                        # try to get the multiplicity
                        try:
                            val = loaded_json['molecule']['multiplicity']
                            if not val in "N/A":
                                temp.multiplicity = val
                        except:
                            temp.multiplicity = None

                        # try to get the basis_set_name
                        try:
                            temp.basis_set_name = loaded_json['comp_details']['general']['basis_set_name']
                        except:
                            temp.basis_set_name = None

                        # try to get the basis_set_size
                        try:
                            temp.basis_set_size = loaded_json['comp_details']['general']['basis_set_size']
                        except:
                            temp.basis_set_size = None

                        # try to get the solvent_method
                        try:
                            temp.solvent_method = loaded_json['comp_details']['general']['solvent_reaction_field']
                        except:
                            temp.solvent_method = None

                        # try to get the solvent
                        try:
                            temp.solvent = loaded_json['comp_details']['general']['solvent']
                        except:
                            temp.solvent = None

                        # try to get the starting_energy
                        try:
                            val = loaded_json['molecule']['starting_energy']
                            if not val in "N/A":
                                temp.starting_energy = val
                        except:
                            temp.starting_energy = None

                        # try to get the ending_energy
                        try:
                            val = loaded_json["results"]["wavefunction"]["total_molecular_energy"]
                            if not val in "N/A":
                                temp.ending_energy = val
                        except:
                            temp.ending_energy = None

                        # try to get the HOMO
                        try:
                            val = loaded_json['results']['wavefunction']['homo_indexes']
                            if not val in "N/A":
                                temp.homo.append(val)
                                print(temp.homo)
                        except:
                            temp.homo = None

                        # try to get the solvent_method
                        try:
                            val = loaded_json
                            if not val in "N/A":
                                temp.homo.append(val)
                                print(temp.homo)
                        except:
                            temp.homo = None
                        # getting the CID and the IUPAC
                        try:
                            formule = loaded_json['molecule']['formula']
                            # open the csv
                            csv_file = open(relation_file, 'r')
                            reader = csv.reader(csv_file, delimiter=";")
                            for rows in reader:
                                if formule == rows[1].strip():
                                    temp.cid = rows[0].strip()
                                    temp.iupac = rows[2].strip()  # we make a strip to escape all whitespace
                                    break
                            csv_file.close()
                        except:
                            print('error in parsing the relation file')
                            temp.cid = None
                            temp.cid = None

                        # store the file in data bank
                        temp.files_path = self.store(destination_dir)
                        subprocess.Popen(["cp", path, temp.files_path])#copie du JSON
                        #TODO copie du pdf+jpeg
                        temp.date = datetime.now()
                        temp.save()
                    else:
                        print("cant load " + source_dir+'/'+dir+'/'+filename)

    def handle(self, *args, **options):
        # absolute path to the source directory where are all the data
        source_dir = '/home/etudiant/Documents/stage/data_brice/fchk_log_files'

        # absolute path to the destination directory where we are going to store all the data
        destination_dir = '/home/etudiant/Documents/stage/data_dir/'

        # absolute path to the reation file
        relation_file = '/home/etudiant/Documents/stage/data_brice/names50k.csv'
        self._create_query(source_dir=source_dir,destination_dir=destination_dir,relation_file=relation_file)
