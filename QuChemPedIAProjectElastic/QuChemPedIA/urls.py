from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('query', views.query, name='query'),
    path('auth', views.auth, name='auth'),
    path('logout', views.deconnexion, name='logout'),
    path('details', views.details, name='details'),
    path('details_json', views.details_json, name='details_json'),
    path('details_image', views.details_image, name='details_image'),
    path('rapport/<str:id>', views.rapport, name='rapport'),
    path('dashboard', login_required(views.dashboard), name='dashboard'),
    path('dashboard/account', login_required(views.account), name='dasboard/account'),
    path('dashboard/password', login_required(views.password), name='dashboard/change_password'),
    path('dashboard/import', views.import_view, name='dashboard/import'),
    path('dashboard/history', login_required(views.user_history_import), name='dashboard/history'),
    path('admin', login_required(views.admin), name='admin'),
    path('admin/user_list', login_required(views.list_of_all_user), name='admin/user_list'),
    path('admin/edit_user/<int:id>', login_required(views.admin_edit_user), name='admin/edit_user'),
    path('admin/list_of_import_in_database', login_required(views.list_of_import_in_database),
         name='admin/list_of_import_in_database'),
    path('admin/list_of_rule', login_required(views.edit_rule_admin),
         name='admin/list_of_rule'),
    path('admin/switch_rule/<int:id_of_rule>/<int:page>', login_required(views.switch_rule),
         name='admin/switch_rule'),
    path('admin/launch_import/<str:id_file>/<int:page>', login_required(views.launch_import),
         name='admin/launch_import'),
    path('admin/delete_import/<str:id_file>/<int:page>', login_required(views.delete_import),
         name='admin/delete_import'),
]
