from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    Nom = models.CharField(max_length=20,null=True)
    prenom = models.CharField(max_length=20,null=True)
    tel = models.CharField(max_length=10,null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add a unique related_name here
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Add a unique related_name here
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def __str__(self):
        return f' {self.Nom} {self.prenom}'
    
class Produits(models.Model):  # Utilisation de models.Model au lieu d'AbstractUser
    TYPE_CHOICES = [
        ('salé', 'Salé'),
        ('gateaux', 'Gateaux'),
        ('tartes', 'Tartes'),
        ('venoiserie', 'Venoiserie'),
        ('confisserie', 'Confisserie'),
        ('snack', 'Snack'),
        ('glaces', 'Glaces'),
        ('gateau_trad', 'Gateau_trad'),
    ]
    Nom = models.CharField(max_length=200)  # Augmentation de la taille du champ pour être cohérent avec le formulaire
    description = models.TextField(max_length=255, null=True)
    prix = models.IntegerField(null=True)  # Suppression de max_length, qui n'est pas applicable à IntegerField
     # Suppression de max_length, qui n'est pas applicable à IntegerField
    Disponibilité = models.BooleanField(default=True)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.type} : {self.Nom}'
    
class News(models.Model):  # Utilisation de models.Model au lieu d'AbstractUser
    
    Nom = models.CharField(max_length=200)  # Augmentation de la taille du champ pour être cohérent avec le formulaire
    description = models.TextField(max_length=255, null=True)
    # Suppression de max_length, qui n'est pas applicable à IntegerField
    # Suppression de max_length, qui n'est pas applicable à IntegerField
   
    image = models.ImageField(upload_to='News/', null=True, blank=True)

    

    def __str__(self):
        return f' {self.Nom}'
    
class Commande(models.Model):  
    TYPE_CHOICES = [
        ('en ligne', 'En Ligne'),
        ('especes', 'Especes'),
    ]
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    Client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    methode_paiement = models.CharField(max_length=50, choices=TYPE_CHOICES)
    payé=models.BooleanField(default=0)
    prix = models.IntegerField(null=True)  
    Quantité = models.IntegerField(null=True) 
    libellé=models.TextField(null=True,max_length=255)
    date_de_commande = models.DateTimeField(default=timezone.now)
    livré=models.BooleanField(default=0)
    def __str__(self):
        return f' produit commandé: {self.produit.Nom} ,pour Monsieur: {self.Client.Nom}{self.Client.prenom}'
    
class Commande_Panier(models.Model):  
   
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    Client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prix = models.IntegerField(null=True)  
    Quantité = models.IntegerField(null=True) 
    libellé=models.TextField(null=True,max_length=255)

    def __str__(self):
        return f' produit commandé: {self.produit.Nom} ,pour Monsieur: {self.Client.Nom}{self.Client.prenom}'
    
