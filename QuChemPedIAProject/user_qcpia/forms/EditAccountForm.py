from django import forms
from user_qcpia.models.UserModel import Utilisateur


class EditUtilisateur(forms.ModelForm):
    """form to allow the user to edit himself is data"""
    def __init__(self, user=None, *args, **kwargs):
        try:
            self.user = user
        except Exception as error:
            self.user=None
            print(error)
        super(EditUtilisateur, self).__init__(*args, **kwargs)
        first_name = None
        last_name = None
        orcid = None
        email = None
        affiliation = None
        city = None
        country = None
        if hasattr(self.user, 'first_name'):
            first_name = self.user.first_name

        if hasattr(self.user, 'last_name'):
            last_name = self.user.last_name

        if hasattr(self.user, 'orcid'):
            orcid = self.user.orcid

        if hasattr(self.user, 'email'):
            email = self.user.email

        if hasattr(self.user, 'affiliation'):
            affiliation = self.user.affiliation

        if hasattr(self.user, 'city'):
            city = self.user.city

        if hasattr(self.user, 'country'):
            country = self.user.country

        self.fields['first_name'] = forms.CharField(label="first name", required=False, widget=(forms.TextInput(
                                                    attrs={'value': first_name or None})))
        self.fields['last_name'] = forms.CharField(label="last name", required=False, widget=(forms.TextInput(
                                                   attrs={'value': last_name or None})))
        self.fields['email'] = forms.CharField(label="email", required=False, widget=(forms.TextInput(
                                               attrs={'value': email or None})))
        self.fields['orcid'] = forms.CharField(label="orcid number", required=False, widget=(forms.TextInput(
                                               attrs={'value': orcid or None})))
        self.fields['affiliation'] = forms.CharField(label="current affiliation", required=False, widget=(forms.TextInput(
                                                     attrs={'value': affiliation or None})))
        self.fields['city'] = forms.CharField(label="city", required=False, widget=(forms.TextInput(
                                                     attrs={'value': city or None})))
        self.fields['country'] = forms.CharField(label="country", required=False, widget=(forms.TextInput(
                                                     attrs={'value': country or None})))

    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'email', 'orcid', 'affiliation', 'city',)
