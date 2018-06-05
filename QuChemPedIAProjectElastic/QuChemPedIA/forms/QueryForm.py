from django import forms


class QueryForm(forms.Form):
    """
        The purpose of this form is to make research in the elasticsearch database
    """
    CHOICES = (('Formula', 'Formula'),
               ('InChi', 'InChi'),
               ('IUPAC', 'IUPAC'),
               ('CID', 'CID'),
               ('SMILES', 'SMILES'),
               ('id_log', 'id_log'),
               # ('homo_alpha_energy', 'homo_alpha_energy'),
               # ('homo_beta_energy', 'homo_beta_energy'),
               # ('lumo_alpha_energy', 'lumo_alpha_energy'),
               # ('lumo_beta_energy', 'lumo_beta_energy')
               )

    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=500, label="",
                             required=False)
    typeQuery = forms.CharField(widget=forms.Select(choices=CHOICES, attrs={'class': 'custom-select'}), label="",
                                required=False,)

    """def clean_query(self):
        #use to reject some key words
        message = self.cleaned_data['query']
        if "pizza" in message:
            raise forms.ValidationError("On ne veut pas entendre parler de pizza !")

        return message  #Ne pas oublier de renvoyer le contenu du champ traité"""
