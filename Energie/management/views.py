from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from management.forms import CompanyForm,CompteurForm
from management.models import  Societe,Compte
from django.core.exceptions import ValidationError
import csv
from datetime import datetime
from .models import Dynef
from django.urls import reverse
from .models import Societe, Compteur
from django.http import HttpResponseRedirect

# Création d'un compte utilisateur
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('prenom')
            user.last_name = form.cleaned_data.get('nom')
            user.save()
            return redirect('/')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
#Système de connexion d'un compte utilisateur
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password) # use username instead of email
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            msg = 'Invalid email or password' # update error message
            form = AuthenticationForm(request.POST)
            messages.error(request, msg) # add error message to messages
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
  
def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    return render(request,'home.html')

#Ajout d'une société
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            societe = form.save(commit=False)
            try:
                #compte = Compte.objects.get(pk=compte_id)
                #print(compte)
                #societe.compte = compte
                societe.save()
                messages.success(request, 'La société a été créée avec succès.')
                return redirect('/')
            except ValidationError as e:
                form.add_error('siret', e)
  
    else:
        form = CompanyForm()
    context = { 'form': form}
    return render(request, 'Societe/add_company.html', context)

#Obtenir toutes les sociétés par compte
def get_societes_by_compte(request, compte_id):
    compte = Compte.objects.get(id=compte_id)
    societes = Societe.objects.filter(compte=compte)
    context = {
        'compte': compte,
        'societes': societes
    }
    return render(request, 'Societe/societes.html', context)

# Obtenir une société par son Siret
def search_by_siret(request):
        siret = request.POST['siret']
        societe = Societe.objects.get(siret=siret)
        context = {
            'societe': societe
        }
        return render(request, 'Societe/societe.html', context)



def get_societe_by_siret(request,siret):
    siret = request.GET.get('siret')

    societe = Societe.objects.get(siret=siret)
    context = {
        'societe': societe
    }
    return render(request, 'Societe/societe.html', context)

# Ajouter un compteur à une société
def Add_compteur(request, siret):
    societe = Societe.objects.get(siret=siret)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            compteur = form.save(commit=False)
            compteur.societe = societe
            compteur.save()
            messages.success(request, 'Le compteur a été créée avec succès.')
        #return HttpResponseRedirect(reverse('societe', args=(siret,)))
            return redirect('/', siret=siret)
    else:
        form = CompteurForm()
    context = {
        'societe': societe,
    }
    return render(request, 'compteurs/Add_compteur.html', context)


def add_data_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)  # Skip the header row

        for row in reader:
            # Assuming the CSV file is in the format provided in the question
            id = row[0]
            prix = row[1].replace(',', '.')  # Replace ',' with '.' for decimal values
            date_debut = datetime.strptime(row[5], '%d/%m/%Y').date()
            date_fin = datetime.strptime(row[7], '%d/%m/%Y').date()
            dynef = Dynef(id=id, prix=prix,  date_debut=date_debut ,date_fin=date_fin)
            dynef.save()
        return render(request, 'Dynef/success.html')
    else:
        return render(request, 'Dynef/upload.html')