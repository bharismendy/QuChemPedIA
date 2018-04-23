from django.contrib import admin
from QuChemPedIA.models.QueryModel import Query

class QueryAdmin(admin.ModelAdmin):
    list_display = ('cid', 'iupac', 'inchi','smiles','formula','path')
    list_filter = ('cid', 'iupac', 'inchi','smiles','formula','path')
    ordering = ('cid', )
    search_fields = ('cid', 'iupac', 'inchi','smiles','formula','path')

admin.site.register(Query,QueryAdmin)