import os
from django.conf import settings
import json


def store_in_temp(id_calcul, file, type):
        """
        method to find the right directory to store data wile it's not processed
        :param id_calcul: id of the calcul in database if none (=0) create a new directory
        :param file: file to import
        :return:
        """
        destination_dir = settings.MEDIA_ROOT+"/to_import/"  # start at media
        number_of_subdir = 5
        cut_number_by = 3
        if len(id_calcul) > number_of_subdir*cut_number_by:
            print("error in the path for id " + id_calcul)
            exit()
        if len(id_calcul) < number_of_subdir*cut_number_by:  # add the subdir
            id_calcul = id_calcul.zfill(number_of_subdir * cut_number_by)

        path_in_file_system = '/'.join(id_calcul[i:i+cut_number_by] for i in range(0, len(id_calcul), cut_number_by))

        try:
            path = destination_dir + path_in_file_system
            if not os.path.isdir(path):
                os.makedirs(destination_dir + path_in_file_system)

            if type == 'json':
                with open(path+"/"+'data.'+type, 'w') as outfile:
                    json.dump(file, outfile)
            else:
                with open(path+'/'+'data.'+type, 'w') as outfile:
                    outfile.write(file)
                    outfile.close()
        except Exception as error:
            print(error)

        return "to_import/"+path_in_file_system+"/"+'data.'+type
