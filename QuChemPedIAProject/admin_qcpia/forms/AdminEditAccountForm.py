from django import forms
from user_qcpia.models.UserModel import Utilisateur


class AdminEditUtilisateur(forms.ModelForm):
    """
    form that allow edit all user so it must only by accessible by admin,
    """
    def __init__(self, user=None, *args, **kwargs):
        """
        constructor of the form from the class AdminEditUtilisateur
        :param user: user object retrieve from db
        :param args: optionnal atguments
        :param kwargs: optionnal argument
        """
        try:
            self.user = user
        except Exception as error:
            print (error)
            self.user = None
        super(AdminEditUtilisateur, self).__init__(*args, **kwargs)

        first_name = None
        last_name = None
        orcid = None
        email = None
        group = None
        last_date_upload = None
        number_of_upload_this_day = None
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

        if not hasattr(self.user, 'admin'):
            admin = False
        else:
            admin = self.user.admin

        if not hasattr(self.user, 'staff'):
            staff = False
        else:
            staff = self.user.staff

        if not hasattr(self.user, 'active'):
            staff = False
        else:
            active = self.user.active

        if hasattr(self.user, 'group'):
            group = self.user.group

        if hasattr(self.user, 'last_date_upload'):
            last_date_upload = self.user.last_date_upload

        if hasattr(self.user, 'number_of_upload_this_day'):
            number_of_upload_this_day = self.user.number_of_upload_this_day

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

        self.fields['group'] = forms.CharField(label="group", required=False, widget=(forms.TextInput(
                                                     attrs={'value': group or None})))

        self.fields['last_date_upload'] = forms.CharField(label="last_date_upload", required=False, widget=(forms.TextInput(
                                                     attrs={'value': last_date_upload or None})))

        self.fields['affiliation'] = forms.CharField(label="current affiliation", required=False, widget=(forms.TextInput(
                                                     attrs={'value': affiliation or None})))

        self.fields['number_of_upload_this_day'] = forms.CharField(label="number of upload today", required=False,
                                                                   widget=(forms.TextInput(
                                                                    attrs={'value': number_of_upload_this_day or None}))
                                                                   )
        self.fields['city'] = forms.CharField(label="city", required=False, widget=(forms.TextInput(
                                                     attrs={'value': city or None})))

        self.fields['country'] = forms.CharField(label="country", required=False, widget=(forms.TextInput(
                                                     attrs={'value': country or None})))

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
                  'number_of_upload_this_day',)
