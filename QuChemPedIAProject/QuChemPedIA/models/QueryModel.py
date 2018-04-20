from django.db import models
import os

class Query(models.Model):
    CID = models.BigIntegerField()
    IUPAC = models.TextField()
    InChi = models.TextField()
    SMILES = models.TextField()
    FormuleBrute = models.TextField()
    Path = models.FilePathField(path=os.path.dirname('/home/etudiant/Documents/stage/data_brice/fchk_log_files'), recursive=True, allow_folders=True)

    class Meta:
        verbose_name = "query"

    def __str__(self):
        return self.IUPAC