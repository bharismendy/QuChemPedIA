from django.db import models
import os

class Query(models.Model):
    CID = models.BigIntegerField()
    IUPAC = models.TextField()
    InChi = models.TextField()
    SMILES = models.TextField()
    Formula = models.TextField()
    method = models.TextField()
    nuclear_starting_energy = models.BigIntegerField()
    nuclear_ending_energy = models.BigIntegerField()
    charge = models.BigIntegerField()
    theory = models.CharField(max_length=10)
    software = models.CharField(max_length=20)
    functional = models.CharField(max_length=20)

    Path = models.FilePathField(path=os.path.dirname('/home/etudiant/Documents/stage/data_brice/fchk_log_files'), recursive=True, allow_folders=True)

    class Meta:
        verbose_name = "query"

    def __str__(self):
        return self.IUPAC