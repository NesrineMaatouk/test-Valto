"""Energie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from management.views import login_view, logout_view,register,home,add_company,get_societes_by_compte,get_societe_by_siret,Add_compteur,add_data_from_csv,search_by_siret


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('add_company/', add_company, name='add_company'),
    path('<int:compte_id>/societes/', get_societes_by_compte, name='societes'),
    path('societe/<str:siret>', get_societe_by_siret, name='societe'),
    path('upload/', add_data_from_csv, name='upload'),
    path('societe/<str:siret>/Add_compteur/', Add_compteur, name='Add_compteur'),
   
    path('', home, name='home'),
]
