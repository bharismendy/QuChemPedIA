from django.shortcuts import render, reverse
from query_qcpia.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from user_qcpia.forms.LoginForm import LoginForm
from user_qcpia.forms.SignUpForm import SignUpForm
from django.contrib.auth import authenticate, login


def auth(request):
    """
    controler that allow the user to login or register on the web site
    :param request: request variable
    :return: a view with both form (login and register)
    """

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
                return HttpResponseRedirect('dashboard/history')
            else:  # sinon une erreur sera affichée
                error_login = True
    else:
        login_form = LoginForm()

    if request.method == 'POST' and 'btn-register' in request.POST:
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('accueil'))

    else:
        register_form = SignUpForm()

    return render(request, 'user_qcpia/auth.html', {'query_form': query_form,
                                                    'register_form': register_form,
                                                    'login_form': login_form,
                                                    'error_login': error_login,
                                                    'error_register': error_register})

