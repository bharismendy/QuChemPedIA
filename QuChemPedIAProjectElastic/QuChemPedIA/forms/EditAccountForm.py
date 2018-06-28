from django import forms
from QuChemPedIA.models.UserModel import Utilisateur


class EditUtilisateur(forms.ModelForm):
    def __init__(self, user = None, *args, **kwargs):
        try:
            self.user = user
        except:
            self.user=None
        super(EditUtilisateur, self).__init__(*args, **kwargs)
        if not hasattr(self.user, 'first_name'):
            first_name = "My first name"
        else:
            first_name = self.user.first_name

        if not hasattr(self.user, 'last_name'):
            last_name = "My last name"
        else:
            last_name = self.user.last_name

        if not hasattr(self.user, 'orcid'):
            orcid = "My last name"
        else:
            orcid = self.user.orcid

        if not hasattr(self.user, 'email'):
            email = "My email"
        else:
            email = self.user.email

        if not hasattr(self.user, 'affiliation'):
            affiliation = "My affiliation"
        else:
            affiliation = self.user.affiliation

        self.fields['first_name'] = forms.CharField(label="first name", required=False, widget=(forms.TextInput(
                                                    attrs={'value': first_name})))
        self.fields['last_name'] = forms.CharField(label="last name", required=False, widget=(forms.TextInput(
                                                   attrs={'value': last_name})))
        self.fields['email'] = forms.CharField(label="email", required=False, widget=(forms.TextInput(
                                               attrs={'value': email or None})))
        self.fields['orcid'] = forms.CharField(label="orcid", required=False, widget=(forms.TextInput(
                                               attrs={'value': orcid or None})))
        self.fields['affiliation'] = forms.CharField(label="affiliation", required=False, widget=(forms.TextInput(
                                                     attrs={'value': affiliation or None})))

    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'orcid', 'affiliation',)
