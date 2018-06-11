from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from QuChemPedIA.forms.EditAccountForm import EditUtilisateur
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


def account(request):
    """
    controler of the template account that allow to edit the user profile
    :param request: variable wich contains the value of the page
    :return: template html
    """

    if request.method == 'POST':
        form_edit_password = PasswordChangeForm(data=request.POST, user=request.user)
        form_edit_utilisateur = EditUtilisateur(data=request.POST, user=request.user, instance=request.user)

        if form_edit_password.is_valid():
            user = form_edit_password.save()
            update_session_auth_hash(request, user)  # Important!

        if form_edit_utilisateur.is_valid():
            form_edit_utilisateur.save()
    else:
        form_edit_password = PasswordChangeForm(request.user)
        form_edit_utilisateur = EditUtilisateur(data=request.POST, user=request.user)
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/account.html', locals())
