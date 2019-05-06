from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from import_qcpia.views import importView

urlpatterns = [
    path('admin', login_required(views.admin), name='admin'),
    path('admin/user_list', login_required(views.list_of_all_user), name='admin/user_list'),
    path('admin/edit_user/<int:id>', login_required(views.admin_edit_user), name='admin/edit_user'),
    path('admin/list_of_import_in_database', login_required(views.list_of_import_in_database),
         name='admin/list_of_import_in_database'),
    path('admin/list_of_rule', login_required(views.edit_rule_admin),
         name='admin/list_of_rule'),
    path('admin/switch_rule/<int:id_of_rule>/<int:page>', login_required(views.switch_rule),
         name='admin/switch_rule'),
    path('admin/launch_import/<str:id_file>/<int:page>', login_required(importView.launch_import),
         name='admin/launch_import'),
    path('admin/delete_import/<str:id_file>/<int:page>', login_required(importView.delete_import),
         name='admin/delete_import'),
]
