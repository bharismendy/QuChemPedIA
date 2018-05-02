from builtins import print
from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import random
"""
    Utilisation de cette commande :
                            -activer le virtualenv (source venv/bin/activate
                            -mettez à jour le destination_dir et le source dir
                            -mettez à jour la base de donnée avec les commandes suivantes :
                                -python manage.py makemigrations QuChemPedIA
                                -python manage.py migrate
                            -déplacez vous dans le dossier QuChemPedIAProject 
                            -entrer dans le terminal la commande : python manage.py testDB
                -> version : 2.3
"""


class Command(BaseCommand):

    def __create_query(self):
        nb_created = 0
        nb_of_primary_element = 232
        nb_element = 10000-nb_of_primary_element

        while nb_created < nb_element:
            # get element betwin 0 and 232(number of primary element in DB
            id = random.randint(1, nb_of_primary_element)
            query = Query.objects.get(id_log=id)
            try:
                nb_created +=1
                query.id_log = nb_created+nb_of_primary_element
                query.save()
                print(nb_created)
            except Exception as error:
                print(error)

    def handle(self, *args, **options):
        self.__create_query()
