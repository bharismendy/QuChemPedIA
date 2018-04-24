from django.db import models
from django.contrib.postgres.fields import ArrayField

class Query(models.Model):
    #base
    id_log = models.BigAutoField(primary_key=True)
    date = models.DateField()
    files_path = models.FilePathField(allow_folders=True)

    #description
    cid = models.BigIntegerField(default=None,null=True)
    iupac = models.TextField(default=None,null=True)
    inchi = models.TextField(default=None)
    smiles = models.TextField(default=None)
    cansmiles = models.CharField(max_length=100, default=None)
    formula = models.TextField(default=None,null=True)#todo null ?
    charge = models.IntegerField(default=None)
    multiplicity = models.IntegerField(default=None)

    #computational details
    method = models.TextField(default=None)
    theory = models.CharField(max_length=10, default=None)#todo table ?
    software = models.CharField(max_length=20, default=None)#todo table ?
    functional = models.CharField(max_length=20, default=None)#todo code/table ?
    basis_set_name = models.CharField(max_length=100, default=None, null=True)
    basis_set_size = models.IntegerField(default=None)
    solvent_method = models.CharField(max_length=100, default=None, null=True)
    solvent = models.CharField(max_length=100, default='GAS')

    #energy and result
    nuclear_starting_energy = models.BigIntegerField(default=None)
    nuclear_ending_energy = models.BigIntegerField(default=None)
    starting_energy = models.IntegerField(default=None,null=True)
    ending_energy = models.IntegerField(default=None,null=True)
    homo = ArrayField(base_field=models.IntegerField(default=None), default=None,null=True)
    lumo = models.FloatField(default=None,null=True)

    """
        Django demandant des valeurs par défaut pour chaque attribut je met par defaut la valeur null mais si je n'autorise pas cette valeur 
        il génère une erreur à l'insertion en base de données 
    """
    class Meta:
        verbose_name = "query"

    def __str__(self):
        return self.iupac