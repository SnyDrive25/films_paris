from unicodedata import name
from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('rechercher', views.rechercher, name='rechercher'),
]