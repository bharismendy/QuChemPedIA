from builtins import print

from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import os
import json
import csv


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


    def store(self, destination_dir, path):
        id = Query.objects.count()
        list_dir = os.listdir(destination_dir)
        last = False
        while(not last):
            list_dir = self.cleanFile(list_dir,path)
            if(len(list_dir)==0):  # test si on est arrivé au dernier dossier
                last = True
                break
            else :
                list_dir.sort()
                list_dir = self.cleanFile(list_dir,path)
                path = path+"/"+list_dir[len(list_dir)-1]
                list_dir = os.listdir(path=path)
        print(path)
        if len(list_dir)<25000:
            # make dir
            print("")


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
                            temp.InChi = loaded_json['molecule']['inchi'][0]
                        except:
                            temp.InChi = "N/A"

                        # try to get the formula
                        try:
                            temp.Formula =loaded_json['molecule']['formula']
                        except:
                            temp.Formula = "N/A"

                        # try to get the SMILES
                        try:
                            temp.Formula = loaded_json['molecule']['smi']
                        except:
                            temp.Formula = "N/A"

                        # try to get the theory
                        try:
                            temp.theory = loaded_json['comp_details']['general']['all_unique_theory'][0]
                        except:
                            temp.theory = "N/A"

                        # try to get the functionnal
                        try:
                            temp.functional = loaded_json['comp_details']['general']['functional']
                        except:
                            temp.functional = "N/A"

                        # try to get the software
                        try:
                            temp.software = loaded_json['comp_details']['general']['package']
                        except:
                            temp.software = "N/A"

                        # try to get the nuclear starting energy
                        try:
                            temp.nuclear_starting_energy = loaded_json['comp_details']['molecule']['starting_energy']
                        except:
                            temp.nuclear_starting_energy = "N/A"

                        # getting the CID and the IUPAC
                        try:
                            formule = loaded_json['molecule']['formula']
                            # open the csv
                            csv_file = open(relation_file, 'r')
                            reader = csv.reader(csv_file, delimiter=";")
                            for rows in reader:
                                if formule == rows[1].strip():
                                    temp.CID = rows[0].strip()
                                    temp.IUPAC = rows[2].strip()  # we make a strip to escape all whitespace
                                    break
                            csv_file.close()
                        except:
                            print('error in parsing the relation file')
                            temp.CID = "N/A"
                            temp.CID = "N/A"

                        # store the file in data bank
                        self.store(destination_dir, path)
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
