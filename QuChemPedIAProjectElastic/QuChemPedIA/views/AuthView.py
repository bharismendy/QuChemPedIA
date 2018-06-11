from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from QuChemPedIA.forms.LoginForm import LoginForm
from QuChemPedIA.forms.SignUpForm import SignUpForm
from django.contrib.auth import authenticate, login


def auth(request):
    query_form = QueryForm(request.GET or None)
    error_login = False
    error_register = False
    if query_form.is_valid():
        return HttpResponseRedirect('query')
    if request.method == 'POST' and 'btn-login' in request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data["email"]
            password = login_form.cleaned_data["password"]
            user = authenticate(email=email, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                return HttpResponseRedirect('accueil')
            else:  # sinon une erreur sera affichée
                error_login = True
    else:
        login_form = LoginForm()

    if request.method == 'POST' and 'btn-register' in request.POST:
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            email = register_form.cleaned_data.get('email')
            raw_password = register_form.cleaned_data.get('password1')
            login(request, user)
            return HttpResponseRedirect('accueil')

    else:
        register_form = SignUpForm()

    return render(request, 'QuChemPedIA/auth.html', locals())

