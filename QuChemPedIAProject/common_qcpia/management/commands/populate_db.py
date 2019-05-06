from builtins import print
from django.core.management.base import BaseCommand
from common_qcpia.QuChemPedIA_lib import import_file
import os


class Command(BaseCommand):

    def _create_query(self, source_dir, id_user):
        """
        this function get all file from the source directory and send them to a function to import them in an
        ElasticSearch
        :param source_dir: directory or file path that contains the new .log
        :param id_user: id of the contributor
        :return: nothing
        """

        get_valid_file = True
        while get_valid_file:
            get_valid_file = False
            for directory in os.listdir(source_dir):
                for filename in os.listdir(source_dir+'/'+directory):
                    if '.json' in filename:
                        path = source_dir+'/'+directory+'/'+filename
                        try:
                            import_file(path=path, id_user=id_user)
                            get_valid_file = True
                        except Exception as error:
                            print(error)
                            get_valid_file = False

    def handle(self, *args, **options):
        # absolute path to the source directory where are all the data
        source_dir = '/home/etudiant/Documents/stage/QuChemPedIAProjectElastic/data_brice3/fchk_log_files'
        id_user = 4

        self._create_query(source_dir=source_dir, id_user=id_user)
