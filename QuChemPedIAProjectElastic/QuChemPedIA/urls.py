from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('query', views.query, name='query'),
    path('details',views.details, name='details'),
    path('details_json/<int:id>',views.details_json, name='details_json'),
    path('rapport/<int:id>', views.rapport, name='rapport'),
]
