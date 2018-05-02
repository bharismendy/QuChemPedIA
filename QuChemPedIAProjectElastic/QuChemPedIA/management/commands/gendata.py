import random
from threading import Thread
from QuChemPedIA.models.QueryModel import Query


class gendata(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, number_of_element, id_dep):
        Thread.__init__(self)
        self.nb_created = 0
        self.id_dep = id_dep+self.nb_created
        self.nb_of_primary_element = 232
        self.nb_element = number_of_element-self.nb_of_primary_element

    def run(self):
        while self.nb_created < self.nb_element:
            # get element betwin 0 and 232(number of primary element in DB
            id = random.randint(1, self.nb_of_primary_element)
            query = Query.objects.get(id_log=id)
            try:
                self.nb_created += 1
                self.id_dep += 1
                query.id_log = self.id_dep
                query.save()
                print(self.nb_created)
            except Exception as error:
                print(error)


class test:
    def __init__(self, nb_data):
        self.test_1(nb_data=nb_data)

    def test_1 (self,nb_data):
        # Création des threads
        to_create = int(nb_data%4)
        id_dep = 0
        nb_launched = int(nb_data / 4) + to_create
        thread_1 = gendata(number_of_element=nb_launched, id_dep=id_dep)
        id_dep = 0 + nb_launched
        nb_launched += int(nb_data / 4)
        thread_2 = gendata(number_of_element=nb_launched, id_dep=id_dep)
        id_dep = 0 + nb_launched
        nb_launched += int(nb_data / 4)
        thread_3 = gendata(number_of_element=nb_launched, id_dep=id_dep)
        id_dep = 0 + nb_launched
        nb_launched += int(nb_data / 4)
        thread_4 = gendata(number_of_element=nb_launched, id_dep=id_dep)

        # Lancement des threads
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        # Attend que les threads se terminent
        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()