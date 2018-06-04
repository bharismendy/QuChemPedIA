from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('accueil', views.accueil, name='accueil'),
    path('query', views.query, name='query'),
    path('details',views.details, name='details'),
    path('details_json/<str:id>',views.details_json, name='details_json'),
    path('details_image/<str:id>',views.details_image, name='details_image'),
    path('rapport/<str:id>', views.rapport, name='rapport'),
]
