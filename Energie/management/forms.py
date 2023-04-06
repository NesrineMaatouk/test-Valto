from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from management.models import Societe,Compteur




class UserRegistrationForm(UserCreationForm):
    nom = forms.CharField(max_length=30, required=True)
    prenom = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('nom', 'prenom', 'email', 'password1', 'password2')

class CompanyForm(forms.ModelForm):
    siret = forms.CharField(max_length=100, required=True)
    raison_sociale = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Societe
        fields = ('siret','raison_sociale')

class CompteurForm(forms.ModelForm):
    num_compteur = forms.CharField(max_length=100, required=True)
    typeEnergie = forms.CharField(max_length=100, required=True)
    consommation= forms.CharField(max_length=100, required=True)
    class Meta:
        model = Compteur
        fields = ['num_compteur', 'typeEnergie', 'consommation']