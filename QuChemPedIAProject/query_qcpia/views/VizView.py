from django.shortcuts import render
from django.conf import settings


def viz(request):
    data_dir = settings.DATA_DIR_URL
    base_url = settings.SITE_ROOT_URL
    return render(request, 'query_qcpia/viz.html', {'data_dir': data_dir, 'base_url': base_url})
