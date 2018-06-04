from django.db import models
from django.contrib.auth.models import User


class Utilisateur(models.Model):
    # data about the user
    id_user = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, default=None)
    group = models.CharField(max_length=50, default="user")
    affiliation = models.TextField(default=None)
    orcid = models.CharField(max_length=19, default=None, null=True)

    """
        Django demandant des valeurs par défaut pour chaque attribut je met par defaut la valeur null 
        mais si je n'autorise pas cette valeur il génère une erreur à l'insertion en base de données
    """
    class Meta:
        verbose_name = "utilisateur"

    def __str__(self):
        return self.user.username
