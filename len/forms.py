from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import CustomUser,Produits
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime,timedelta
from datetime import datetime
from .models import CustomUser 
from django.db.models import Q
from django.utils import timezone
from django.db.models import OuterRef, Exists, Subquery
from django.db.models.functions import Lower
class EmailAuthenticationForm(forms.Form):
    username = forms.CharField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            'placeholder': 'Email',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6',
            'placeholder': 'Mot de passe',
            'autocomplete': 'current-password'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    Prenom = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )
    Nom = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Inform a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )
    tel = forms.CharField(
        max_length=15,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'block w-full rounded-md border-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-700 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6'})
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Cet email est déjà utilisé.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.Nom = self.cleaned_data['Nom']
        user.prenom = self.cleaned_data['Prenom']
        user.tel = self.cleaned_data['tel']

        if commit:
            user.save()
        return user
    
class AddSaléForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
   
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddSaléForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'salé'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
    
class AddGateauForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )

class AddGateauTraditionnelForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
    
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddGateauTraditionnelForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'gateaux'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
    
class AddtartesForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
    
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddtartesForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'tartes'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit

class AddvenoiserieForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
   
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddvenoiserieForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'venoiserie'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
class AddconfisserieForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
   
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddconfisserieForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'confisserie'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
class AddsnackForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
    
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix']
    def __init__(self, *args, **kwargs):
        super(AddsnackForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'snack'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
class AddglacesForm(forms.ModelForm):
    Nom = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm',
            'rows': 4,
            'placeholder': 'Enter the description here...'
        }),
        max_length=255,
        required=True,
        help_text='Required'
    )
    image = forms.ImageField(
        required=True,
        help_text='Required',
        widget=forms.ClearableFileInput(attrs={
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 focus:file:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        })
    )
    prix = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-gray-300 py-2 text-gray-900 shadow-sm focus:ring-yellow-600 focus:border-yellow-600 sm:text-sm'
        }),
        max_length=200,
        required=True,
        help_text='Required'
    )
    
    
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix', ]
    def __init__(self, *args, **kwargs):
        super(AddglacesForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        
    def save(self, commit=True):
        produit = super().save(commit=False)
        produit.type = 'glaces'  # Assurez-vous que le type est défini correctement ici
        if commit:
            produit.save()
        return produit
  
class SaléForm(forms.ModelForm):
    class Meta:
        model = Produits
        fields = ['Nom', 'description', 'image', 'prix' ]
        widgets = {
            'Nom': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-file'}),
            'prix': forms.TextInput(attrs={'class': 'form-input'}),
            
        } 

    def __init__(self, *args, **kwargs):
        super(SaléForm, self).__init__(*args, **kwargs)
        self.fields['prix'].required = False
        