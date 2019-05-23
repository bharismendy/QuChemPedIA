from django import forms


class QueryForm(forms.Form):
    """
        The purpose of this form is to make research in the elasticsearch database
    """
    CHOICES = (('Formula', 'Formula'),
               ('InChi', 'InChi'),
               ('IUPAC', 'IUPAC name'),
               ('CID', 'CID PubChem'),
               ('SMILES', 'SMILES'),
               ('id_log', 'id_log'),
               # ('homo_alpha_energy', 'homo_alpha_energy'),
               # ('homo_beta_energy', 'homo_beta_energy'),
               # ('lumo_alpha_energy', 'lumo_alpha_energy'),
               # ('lumo_beta_energy', 'lumo_beta_energy')
               )

    search = forms.CharField(widget=forms.TextInput(attrs={'id': 'research_entry', 'class' : 'mr-1  col-12 col-lg-6 form-control'}),
                             max_length=500, label="", required=False)
    typeQuery = forms.CharField(widget=forms.Select(choices=CHOICES, attrs={'class': 'form-control                                                                                                           col-12 col-lg-3'}), label="",
                                required=False,)

