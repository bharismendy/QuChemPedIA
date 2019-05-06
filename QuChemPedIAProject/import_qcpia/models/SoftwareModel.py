from django.db import models


class Software(models.Model):
    """this class define the table where the name of software are stored"""
    id_software = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, default=None, null=False)

    class meta:
        verbose_name = "Software"

    def __str__(self):
        return str(self.id_software)
