from django.db import models
from QuChemPedIA.models.UserModel import Utilisateur
from QuChemPedIA.models.SoftwareModel import Software
from QuChemPedIA.models.VersionModel import SoftwareVersion


class ImportFile(models.Model):
    id_file =  models.BigAutoField(primary_key=True)
    id_user = models.ForeignKey(Utilisateur, null=True, default=None, on_delete=models.SET_NULL)  # si null -> anonymous
    path_file = models.FilePathField(default=None, null=False)  # must be fill
    status = models.CharField(max_length=100, default="Stand-by", null=False)
    id_software = models.ForeignKey(Software, null=True, default=None, on_delete=models.SET_NULL)  # si null -> anonymous
    id_version = models.ForeignKey(SoftwareVersion, null=True, default=None, on_delete=models.SET_NULL)  # si null -> anonymous

    class meta:
        verbose_name = "imported file"

    def __str__(self):
        return self.id_file
