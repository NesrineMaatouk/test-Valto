from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class MyCompteManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Compte(AbstractBaseUser):
    email = models.EmailField()
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    class Meta:
        db_table = 'Compte'



class Societe(models.Model):
    siret = models.CharField(max_length=14, unique=True)
    raison_sociale = models.CharField(max_length=100)
    #compte = models.ForeignKey(Compte, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and Societe.objects.filter(siret=self.siret).exists():
            raise ValidationError("La société avec le siret '{}' existe déjà.".format(self.siret))
        super(Societe, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Societe'

class Compteur(models.Model):
    num_compteur = models.CharField(max_length=100)    
    TYPE_ENERGIE_CHOICES = (
        ('D', 'Dynef'),
        ('T', 'TotalEnergie'),
    )
    typeEnergie = models.CharField(max_length=1, choices=TYPE_ENERGIE_CHOICES)
    consommation = models.FloatField()
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Compteur'

class TotalEnergie(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    class Meta:
        db_table = 'TotalEnergie'

class HistoriqueCalcule(models.Model):
    date_today = models.DateField()
    resultat = models.FloatField()
    total_energie = models.ForeignKey(TotalEnergie, on_delete=models.CASCADE)
    dynef = models.ForeignKey('Dynef', on_delete=models.CASCADE)
    class Meta:
        db_table = 'HistoriqueCalcule'

class Dynef(models.Model):
    prix = models.FloatField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    class Meta:
        db_table = 'Dynef'
