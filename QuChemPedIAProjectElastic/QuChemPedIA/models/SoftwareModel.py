from django.db import models


class software(models.Model):
    # data about the user
    id_software = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, default=None)

    class Meta:
        verbose_name = "software"

    def __str__(self):
        return self.name