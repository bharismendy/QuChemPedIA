from django.urls import path
from . import views
from import_qcpia import views as views_import
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('logout', views.deconnexion, name='logout'),
    path('dashboard', login_required(views.dashboard), name='dashboard'),
    path('dashboard/account', login_required(views.account), name='dasboard/account'),
    path('dashboard/history', login_required(views.user_history_import), name='dashboard/history'),
    path('dashboard/import', views_import.import_view, name='dashboard/import'),
]

