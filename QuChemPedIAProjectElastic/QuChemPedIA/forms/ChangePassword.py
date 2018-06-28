from django import forms
from QuChemPedIA.models.UserModel import Utilisateur
from django.core.validators import RegexValidator


class ChangePassword(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        my_validator = RegexValidator(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+!*$@%_])([-+!*$@%_\w]{8,15})$",
                                      ["Your password should contains :",
                                       "- 1 special character",
                                       "- 1 lower caser",
                                       "- 1 upper case",
                                       "- 1 numeric"])
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(label='password * ', required=False, widget=forms.PasswordInput,
                                                  validators=[my_validator])
        self.fields['password2'] = forms.CharField(label='Confirm password * ', required=False, widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ('password',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ChangePassword, self).save(commit=False)
        print(user)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user