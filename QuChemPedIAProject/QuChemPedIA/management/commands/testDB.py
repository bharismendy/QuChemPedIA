from builtins import print

from QuChemPedIA.models.QueryModel import Query
from django.core.management.base import BaseCommand
import os
import json
import csv
import subprocess
from datetime import datetime


class Command(BaseCommand):

    def _create_query(self,source_dir,destination_dir,relation_file):
        print("hello!")

    def handle(self, *args, **options):
        self._create_query(source_dir=source_dir,destination_dir=destination_dir,relation_file=relation_file)
