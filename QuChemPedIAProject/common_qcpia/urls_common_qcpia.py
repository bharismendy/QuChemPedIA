from django.urls import path
from . import views
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
]
