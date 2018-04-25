from django.db import models


class JobType(models.Model):
    # data about the user
    id_job_type = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, default=None)


    """
        Django demandant des valeurs par défaut pour chaque attribut je met par defaut la valeur null mais si je n'autorise pas cette valeur
        il génère une erreur à l'insertion en base de données
    """
    class Meta:
        verbose_name = "job_type"

    def __str__(self):
        return self.name