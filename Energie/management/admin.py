# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Compte, Societe,Compteur
from .models import Dynef

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'prenom', 'nom', 'password','is_active')
    
    def prenom(self, obj):
        return obj.first_name
    
    def nom(self, obj):
        return obj.last_name

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class SociteAdmin(admin.ModelAdmin):
    list_display = ['id', 'siret','raison_sociale']
    search_fields = ['raison_sociale', 'siret']
admin.site.register(Societe, SociteAdmin)

class CompteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'num_compteur', 'typeEnergie', 'consommation','societe')
admin.site.register(Compteur, CompteurAdmin)

