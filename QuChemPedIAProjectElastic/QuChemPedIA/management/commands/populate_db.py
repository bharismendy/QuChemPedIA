from builtins import print
from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import os
import json
from elasticsearch import Elasticsearch
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

    def _create_query(self, source_dir, destination_dir, relation_file):
        # iterate on all file
        i = 0
        # setting conection to elastic search server
        ES_HOST = {"host": "localhost", "port": 9200}
        es = Elasticsearch(hosts=[ES_HOST])

        # creating the index
        INDEX_NAME = 'quchempedia_index'
        if not es.indices.exists(index=INDEX_NAME):
            try :
                response = es.indices.create(index=INDEX_NAME)
                print(response)
            except Exception as error:
                print(error)
        for directory in os.listdir(source_dir):
            for filename in os.listdir(source_dir+'/'+directory):
                if '.json' in filename:
                    path = source_dir+'/'+directory+'/'+filename
                    jsonfile = open(path)
                    if self.is_json(path):
                        try:
                            loaded_json = json.load(jsonfile)
                            content = json.dumps(loaded_json, indent=4, sort_keys=True)
                            i += 1

                            # TODO inscrire l'id du document dans le json ou remplacer par l'id d'elastic de search
                            resp = es.index(index=INDEX_NAME, doc_type="log_file", body=content, id=i)
                        except Exception as error:
                            print(error)
                    else:
                        print("cant load " + source_dir+'/'+directory+'/'+filename)

    def handle(self, *args, **options):
        # absolute path to the source directory where are all the data
        source_dir = '/home/etudiant/Documents/stage/data_brice2/fchk_log_files'

        # absolute path to the destination directory where we are going to store all the data
        destination_dir = '/home/etudiant/Documents/stage/data_dir/'

        # absolute path to the reation file
        relation_file = '/home/etudiant/Documents/stage/data_brice/names50k.csv'
        self._create_query(source_dir=source_dir, destination_dir=destination_dir, relation_file=relation_file)
