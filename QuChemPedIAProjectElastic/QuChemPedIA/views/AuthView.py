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
        print("login")
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
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
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('accueil')
        print("register")

    else:
        register_form = SignUpForm()

    return render(request, 'QuChemPedIA/auth.html', locals())

