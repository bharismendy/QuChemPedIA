from django.db import models
from QuChemPedIA.models.SoftwareModel import Software
from QuChemPedIA.models.VersionModel import SoftwareVersion


class ImportRule(models.Model):
    id_rule = models.BigAutoField(primary_key=True)
    id_software = models.OneToOneField(Software, null=False, unique=False, default=None, on_delete=models.SET_DEFAULT)
    id_version = models.OneToOneField(SoftwareVersion, null=False, unique=False, default=None, on_delete=models.SET_DEFAULT)
    rule = models.CharField(max_length=40, default="manual", null=False)

    class Meta:
        verbose_name = "rule of import"

    def __str__(self):
        return str(self.id_rule)
