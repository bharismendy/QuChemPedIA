from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('query', views.query, name='query'),
    path('details/<int:id>',views.details, name='details'),
    path('rapport/<int:id>', views.rapport, name='rapport'),
]