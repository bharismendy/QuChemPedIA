from django import forms
from QuChemPedIA.models import Utilisateur
from django.core.validators import RegexValidator


class SignUpForm(forms.ModelForm):
    my_validator = RegexValidator(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+!*$@%_])([-+!*$@%_\w]{8,15})$",
                                  ["Your password should contains :",
                                   "- 1 special character",
                                   "- 1 lower caser",
                                   "- 1 upper case",
                                   "- 1 numeric"])
    email = forms.CharField(label='email * ', required=False)
    password1 = forms.CharField(label='password * ', widget=forms.PasswordInput, validators=[my_validator])
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

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
