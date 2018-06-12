import os
import subprocess
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def store_in_temp(id_calcul,file):
        """
        method to find the right directory to store data wile it's not processed
        :param destination_dir: root directory
        :param id_calcul: id of the calcul in database if none (=0) create a new directory
        :param if set to true, create the directory in file system
        :return:
        """
        destination_dir = "to_import/"  # start at media
        number_of_subdir = 5
        path_in_file_system = ''
        cut_number_by = 3
        if len(id_calcul) > number_of_subdir*cut_number_by:
            print("error in the path for id " + id_calcul)
            exit()
        if len(id_calcul) < number_of_subdir*cut_number_by:  # add the subdir
            id_calcul = id_calcul.zfill(number_of_subdir * cut_number_by)

        path_in_file_system = '/'.join(id_calcul[i:i+cut_number_by] for i in range(0, len(id_calcul), cut_number_by))

        try:
            os.makedirs(destination_dir + path_in_file_system)
            path = default_storage.save(destination_dir+path_in_file_system+"/"+file.name, ContentFile(file.read()))
        except Exception as error:
            print(error)

        return destination_dir + path_in_file_system + file.name
