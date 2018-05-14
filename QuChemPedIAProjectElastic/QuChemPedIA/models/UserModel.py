from django.db import models


class utilisateur(models.Model):
    # data about the user
    id_user = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100,default=None)
    affiliation = models.TextField(default=None)
    #TODO DOI && link to log file
    orcid = models.CharField(max_length=19, default=None, null=True)

    """
        Django demandant des valeurs par défaut pour chaque attribut je met par defaut la valeur null 
        mais si je n'autorise pas cette valeur il génère une erreur à l'insertion en base de données
    """
    class Meta:
        verbose_name = "utilisateur"

    def __str__(self):
        return self.name