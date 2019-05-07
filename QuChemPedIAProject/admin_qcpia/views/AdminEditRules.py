from query_qcpia.forms.QueryForm import QueryForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from import_qcpia.models import ImportRule
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common_qcpia.QuChemPedIA_lib import build_url


def edit_rule_admin(request):
    """
    controler of the template account that allow the to edit import rule
    :param request: variable wich contains the value of the page
    :return: template html
    """
    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))
    query_form = QueryForm(request.GET or None)
    page = request.GET.get('page', 1)
    paginator = None
    try:  # get all imported  file
        list_of_rules = ImportRule.objects.all()
        paginator = Paginator(list_of_rules.order_by("id_rule"), 10)
    except Exception as error:
        print(error)
    try:
        rules = paginator.page(page)
    except PageNotAnInteger:
        rules = paginator.page(1)
    except EmptyPage:
        rules = paginator.page(paginator.num_pages)
    if request.GET and 'button-search' in request.GET:
        if query_form.is_valid():
            return HttpResponseRedirect(reverse('query'))

    return render(request, 'admin_qcpia/admin_edit_rule_import.html', {'query_form': query_form,
                                                                       'rules': rules})


def switch_rule(request, id_of_rule, page):

    if not request.user.is_admin:  # security to redirect user that aren't admin
        return HttpResponseRedirect(reverse('accueil'))
    rule_to_switch = ImportRule.objects.get(id_rule=id_of_rule)
    if request.POST:
        rule_to_switch.rule = request.POST.get('options')
        rule_to_switch.save()
    url = build_url('admin/list_of_rule', get={'page': request.GET.get(str(page))})
    return HttpResponseRedirect(url)