from django import forms


class QueryForm(forms.Form):
    """
        The purpose of this form is to make research in the elasticsearch database
    """
    CHOICES = (('CID', 'CID'),
               ('InChi', 'InChi'),
               ('IUPAC', 'IUPAC'),
               ('Formula', 'Formula'),
               ('SMILES', 'SMILES'),
               ('id_log', 'id_log'),
               # ('homo_alpha_energy', 'homo_alpha_energy'),
               # ('homo_beta_energy', 'homo_beta_energy'),
               # ('lumo_alpha_energy', 'lumo_alpha_energy'),
               # ('lumo_beta_energy', 'lumo_beta_energy')
               )
    search = forms.CharField(max_length=500, label="your research", required=True)
    typeQuery = forms.CharField(widget=forms.Select(choices=CHOICES))

    """def clean_query(self):
        #use to reject some key words
        message = self.cleaned_data['query']
        if "pizza" in message:
            raise forms.ValidationError("On ne veut pas entendre parler de pizza !")

        return message  #Ne pas oublier de renvoyer le contenu du champ traité"""
