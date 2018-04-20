from django.contrib import admin
from QuChemPedIA.models.QueryModel import Query

class QueryAdmin(admin.ModelAdmin):
    list_display = ('CID', 'IUPAC', 'InChi','SMILES','FormuleBrute','Path')
    list_filter = ('CID', 'IUPAC', 'InChi','SMILES','FormuleBrute','Path')
    ordering = ('CID', )
    search_fields = ('CID', 'IUPAC', 'InChi','SMILES','FormuleBrute','Path')

admin.site.register(Query,QueryAdmin)