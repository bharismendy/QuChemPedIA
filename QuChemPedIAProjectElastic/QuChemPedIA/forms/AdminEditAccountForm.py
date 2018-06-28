from django import forms
from QuChemPedIA.models.UserModel import Utilisateur


class AdminEditUtilisateur(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        try:
            self.user = user
        except:
            self.user = None
        super(AdminEditUtilisateur, self).__init__(*args, **kwargs)
        if not hasattr(self.user, 'first_name'):
            first_name = "the first name"
        else:
            first_name = self.user.first_name

        if not hasattr(self.user, 'last_name'):
            last_name = "the last name"
        else:
            last_name = self.user.last_name

        if not hasattr(self.user, 'orcid'):
            orcid = "the last name"
        else:
            orcid = self.user.orcid

        if not hasattr(self.user, 'email'):
            email = "the email"
        else:
            email = self.user.email

        if not hasattr(self.user, 'affiliation'):
            admin = False
        else:
            admin = self.user.admin

        if not hasattr(self.user, 'affiliation'):
            staff = False
        else:
            staff = self.user.staff

        if not hasattr(self.user, 'affiliation'):
            active = False
        else:
            active = self.user.active

        if not hasattr(self.user, 'group'):
            group = "the group"
        else:
            group = self.user.group

        if not hasattr(self.user, 'last_date_upload'):
            last_date_upload = None
        else:
            last_date_upload = self.user.last_date_upload

        if not hasattr(self.user, 'number_of_upload_this_day'):
            number_of_upload_this_day = 0
        else:
            number_of_upload_this_day = self.user.number_of_upload_this_day

        if not hasattr(self.user, 'affiliation'):
            affiliation = "the affiliation"
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

        self.fields['group'] = forms.CharField(label="group", required=False, widget=(forms.TextInput(
                                                     attrs={'value': group or None})))

        self.fields['last_date_upload'] = forms.CharField(label="last_date_upload", required=False, widget=(forms.TextInput(
                                                     attrs={'value': last_date_upload or None})))

        self.fields['affiliation'] = forms.CharField(label="affiliation", required=False, widget=(forms.TextInput(
                                                     attrs={'value': affiliation or None})))

        self.fields['number_of_upload_this_day'] = forms.CharField(label="number of upload today", required=False,
                                                                   widget=(forms.TextInput(
                                                                    attrs={'value': number_of_upload_this_day or None}))
                                                                   )
        if active :
            self.fields['active'] = forms.BooleanField(label="active member", required=False,  widget=
                                                      (forms.CheckboxInput(attrs={'checked': "checked"})))
        else:
            self.fields['active'] = forms.BooleanField(label="active member", required=False)

        if staff :
            self.fields['staff'] = forms.BooleanField(label="staff", required=False,  widget=
                                                      (forms.CheckboxInput(attrs={'checked': "checked"})))
        else:
            self.fields['staff'] = forms.BooleanField(label="staff", required=False)

        if admin :
            self.fields['admin'] = forms.BooleanField(label="administrator", required=False,  widget=
                                                      (forms.CheckboxInput(attrs={'checked': "checked"})))
        else:
            self.fields['admin'] = forms.BooleanField(label="administrator", required=False)

    class Meta:
        model = Utilisateur
        fields = ('first_name',
                  'last_name',
                  'email',
                  'orcid',
                  'affiliation',
                  'admin',
                  'staff',
                  'active',
                  'group',
                  'last_date_upload',
                  'number_of_upload_this_day')