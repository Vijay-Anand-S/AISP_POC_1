from django.urls import path
from .views import search




urlpatterns = [
    path('home/',search, name ='home')

]