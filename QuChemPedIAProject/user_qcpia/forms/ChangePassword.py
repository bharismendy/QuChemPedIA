from django import forms
from user_qcpia.models.UserModel import Utilisateur


class ChangePassword(forms.ModelForm):
    """form to change the password of an user"""
    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.fields['password'] = forms.CharField(label='password * ', required=False, widget=forms.PasswordInput)
        self.fields['password2'] = forms.CharField(label='Confirm password * ', required=False, widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ('password',)

    def clean_password1(self):
        """check if the password is valid"""
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("The password should contains at least 8 characters")
        return password1

    def clean_password2(self):
        """Check that the two password entries match"""

        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """ Save the provided password in hashed format"""
        user = super(ChangePassword, self).save(commit=False)
        print(user)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user