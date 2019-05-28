from django.db import models
from import_qcpia.models.SoftwareModel import Software


class SoftwareVersion(models.Model):
    """allow to store the number of the version"""
    id_version = models.BigAutoField(primary_key=True)
    version_number = models.CharField(max_length=40, null=False, default=None)
    id_software = models.ForeignKey(Software, null=False, default=None, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "software version"

    def __str__(self):
        return str(self.id_version)
