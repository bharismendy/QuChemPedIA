from django import forms


class LoginForm(forms.Form):
    """form to allow a user to log into the website"""
    email = forms.CharField(label="email", max_length=30)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
