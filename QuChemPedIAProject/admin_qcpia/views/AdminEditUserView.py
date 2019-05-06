from query_qcpia.forms.QueryForm import QueryForm
from user_qcpia.forms.ChangePassword import ChangePassword
from admin_qcpia.forms.AdminEditAccountForm import AdminEditUtilisateur
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from user_qcpia.models import Utilisateur


def admin_edit_user(request, id):
    """
    controler to edit all user profile
    :param request: environement variable of http request
    :param id: id of the user
    :return: http response
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))

    current_user = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        if 'btn-admin-update-profil' in request.POST:
            form_edit_utilisateur = AdminEditUtilisateur(data=request.POST, user=current_user, instance=current_user)
            if form_edit_utilisateur.is_valid():
                form_edit_utilisateur.save()
        if 'btn-admin-update-password' in request.POST:
            form_change_password = ChangePassword(data=request.POST, instance=current_user)
            if form_change_password.is_valid():
                form_change_password.save()

    form_edit_utilisateur = AdminEditUtilisateur(data=request.POST, user=current_user, instance=current_user)
    form_change_password = ChangePassword(data=request.POST, instance=current_user)
    query_form = QueryForm(request.GET or None)
    if query_form.is_valid():
        return HttpResponseRedirect(reverse('query'))

    return render(request, 'admin_qcpia/admin_edit_user_profile.html', {'query_form': query_form,
                                                                        'form_edit_utilisateur': form_edit_utilisateur,
                                                                        'form_change_password': form_change_password,
                                                                        'id_user': id})
