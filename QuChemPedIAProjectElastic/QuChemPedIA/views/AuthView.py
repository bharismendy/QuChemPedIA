from django.shortcuts import render
from django.contrib.auth import authenticate, login
from QuChemPedIA.forms.LoginForm import LoginForm


def connexion(request):
    error = False
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else:  # sinon une erreur sera affichée
                error = True
    else:
        login_form = LoginForm()

    return render(request, 'QuChemPedIA/auth.html', locals())