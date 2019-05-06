from django import forms
from user_qcpia.models import Utilisateur


class SignUpForm(forms.ModelForm):
    """form to register a new user"""

    email = forms.CharField(label='email * ', required=False)
    password1 = forms.CharField(label='password * ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password * ', widget=forms.PasswordInput)
    affiliation = forms.CharField(label='affiliation', required=False)

    field_order = ['email', 'password1', 'password2', 'affiliation', ]

    class Meta:
        model = Utilisateur
        fields = ('email', 'affiliation',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Utilisateur.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password1(self):
        """check if the password is valid"""
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("The password should contains at least 8 characters")
        return password1

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        :param commit: True to save in DB false in other case
        :return: the method return a user object to the controleur
        """
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
