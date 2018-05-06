from django.db import models
from .UserModel import utilisateur
from .JobTypeModel import JobType
from .TheoryModel import theory
from .SoftwareModel import software
from .FunctionnalModel import functionnal
#from QuChemPedIA.search import QuChemPedIAIndex


class Query(models.Model):
    #base
    id_log = models.BigAutoField(primary_key=True)
    date = models.DateField()
    files_path = models.FilePathField(allow_folders=True,default=None)

    # lien vers la table utilisateur et job_type
    user = models.ForeignKey(utilisateur, on_delete=models.SET_NULL, null=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_DEFAULT, null=True, default=1)

    #description
    cid = models.BigIntegerField(default=None,null=True)
    iupac = models.CharField(max_length=500,default=None,null=True)
    inchi = models.CharField(max_length=1000,default=None)
    smiles = models.CharField(max_length=500, default=None)
    cansmiles = models.CharField(max_length=500, default=None)
    formula = models.CharField(max_length=30,default=None,null=True)#todo null ?
    charge = models.SmallIntegerField(default=0)
    multiplicity = models.SmallIntegerField(default=None)

    #computational details
    theory = models.ForeignKey(theory, on_delete=models.SET_DEFAULT, null=False, default=None)
    functional = models.ForeignKey(functionnal, on_delete=models.SET_DEFAULT, null=False, default=None)
    software = models.ForeignKey(software, on_delete=models.SET_DEFAULT, null=False, default=None)
    basis_set_name = models.CharField(max_length=20, default=None, null=True)
    basis_set_size = models.IntegerField(default=None)
    solvatation_method = models.CharField(max_length=10, default=None, null=True)
    solvent = models.CharField(max_length=40, default='GAS')

    #energy and result
    starting_nuclear_repulsion_energy = models.FloatField(default=None)
    ending_nuclear_repulsion_energy = models.FloatField(default=None)
    starting_energy = models.FloatField(default=None, null=True)
    ending_energy = models.FloatField(default=None)
    homo_alpha_energy = models.FloatField(default=None,null=True)
    homo_beta_energy = models.FloatField(default=None,null=True)
    lumo_alpha_energy = models.FloatField(default=None, null=True)
    lumo_beta_energy = models.FloatField(default=None, null=True)

    """
        Django demandant des valeurs par défaut pour chaque attribut je met par defaut la valeur null mais si je n'autorise pas cette valeur 
        il génère une erreur à l'insertion en base de données 
    """
    class Meta:
        verbose_name = "query"

    def __str__(self):
        return self.iupac
