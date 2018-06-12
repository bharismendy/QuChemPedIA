from QuChemPedIA.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from QuChemPedIA.forms.EditAccountForm import EditUtilisateur
from django.shortcuts import render


def account(request):
    """
    controler of the template account that allow to edit the user profile
    :param request: variable wich contains the value of the page
    :return: template html
    """

    if request.method == 'POST':
        form_edit_utilisateur = EditUtilisateur(data=request.POST, user=request.user, instance=request.user)
        if form_edit_utilisateur.is_valid():
            form_edit_utilisateur.save()
    else:
        form_edit_utilisateur = EditUtilisateur(data=request.POST, user=request.user)
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect('query')

    return render(request, 'QuChemPedIA/account.html', {'query_form': query_form,
                                                        'form_edit_utilisateur': form_edit_utilisateur})
