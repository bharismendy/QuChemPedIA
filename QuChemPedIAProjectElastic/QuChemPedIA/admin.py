from django.contrib import admin
from QuChemPedIA.models.QueryModel import Query
from QuChemPedIA.models.UserModel import utilisateur
from QuChemPedIA.models.SoftwareModel import software
from QuChemPedIA.models.TheoryModel import theory
from QuChemPedIA.models.FunctionnalModel import functionnal
from QuChemPedIA.models.JobTypeModel import JobType

"""
class QueryAdmin(admin.ModelAdmin):
    list_display = ('cid', 'iupac', 'inchi', 'smiles', 'formula', 'files_path')
    list_filter = ('cid', 'iupac', 'inchi', 'smiles', 'formula', 'files_path')
    ordering = ('cid', )
    search_fields = ('cid', 'iupac', 'inchi', 'smiles', 'formula', 'files_path')
"""
admin.site.register(Query)
admin.site.register(utilisateur)
admin.site.register(software)
admin.site.register(theory)
admin.site.register(functionnal)
admin.site.register(JobType)
