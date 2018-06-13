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
    path('details_json/<str:id>', views.details_json, name='details_json'),
    path('details_image/<str:id>', views.details_image, name='details_image'),
    path('rapport/<str:id>', views.rapport, name='rapport'),
    path('dashboard', login_required(views.dashboard), name='dashboard'),
    path('dashboard/account', login_required(views.account), name='dasboard/account'),
    path('dashboard/password', login_required(views.password), name='dashboard/change_password'),
    path('dashboard/import', views.import_view, name='dashboard/import'),
    path('dashboard/history', login_required(views.user_history_import), name='dashboard/history'),
]
