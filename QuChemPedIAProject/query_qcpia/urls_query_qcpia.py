from django.urls import path
from . import views
urlpatterns = [
    path('query', views.query, name='query'),
    path('details', views.details, name='details'),
    path('details_json', views.details_json, name='details_json'),
    path('details_author', views.details_author, name='details_author'),
    path('details_image', views.details_image, name='details_image'),
    path('rapport/<str:id>', views.rapport, name='rapport'),
    path('viz', views.viz, name='viz')
]
