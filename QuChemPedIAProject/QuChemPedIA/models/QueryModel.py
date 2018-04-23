from django.db import models
from django.contrib.postgres.fields import ArrayField

class Query(models.Model):
    id_log = models.BigAutoField(primary_key=True)
    date = models.DateField()
    cid = models.BigIntegerField(default=None,null=True)
    iupac = models.TextField(default=None,null=True)
    inchi = models.TextField(default=None,null=True)
    smiles = models.TextField(default=None,null=True)
    formula = models.TextField(default=None,null=True)
    method = models.TextField(default=None,null=True)
    nuclear_starting_energy = models.BigIntegerField(default=None, null=True)
    nuclear_ending_energy = models.BigIntegerField(default=None, null=True)
    charge = models.IntegerField(default=None, null=True)
    theory = models.CharField(max_length=10, default=None, null=True)
    software = models.CharField(max_length=20, default=None, null=True)
    functional = models.CharField(max_length=20, default=None,null=True)
    path = models.FilePathField(allow_folders=True, null=True)
    cansmiles = models.CharField(max_length=100, default=None)
    multiplicity = models.IntegerField(default=None, null=True)
    basis_set_name = models.CharField(max_length=100, default=None,null=True)
    basis_set_size = models.IntegerField(default=None,null=True)
    solvent_method = models.CharField(max_length=100, default=None,null=True)
    solvent = models.CharField(max_length=100, default=None,null=True)
    starting_energy = models.IntegerField(default=None,null=True)
    ending_energy = models.IntegerField(default=None,null=True)
    homo = ArrayField(base_field= models.IntegerField(default=None,blank=True), default=None,null=True)

    class Meta:
        verbose_name = "query"

    def __str__(self):
        return self.iupac