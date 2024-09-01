from django.shortcuts import render
from .forms import AddGateauTraditionnelForm,AddglacesForm,AddsnackForm,AddconfisserieForm,AddvenoiserieForm,AddtartesForm,EmailAuthenticationForm,CustomUserCreationForm,AddSaléForm,SaléForm,AddGateauForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import News,Commande_Panier,Produits,Commande
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http.response import HttpResponse
def index(request):
    return render(request, "theme/base.html")
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)  # Enlever `request`
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('len:admine')
                return redirect('len:index') 
            else:
                # Gérer l'erreur si l'utilisateur ne peut pas être authentifié
                form.add_error(None, "email ou mot de passe incorrect")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'theme/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('len:index')  # Assurez-vous que 'login' est bien le nom de votre vue de connexion



def Register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Votre compte a été créé avec succès !')
                return redirect('len:login')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du compte. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'theme/register.html', {'form': form})

@login_required
def admine(request):
    Salé = Produits.objects.filter(type="salé")
    gateaux = Produits.objects.filter(type="gateaux")
    glaces = Produits.objects.filter(type="glaces")
    tartes = Produits.objects.filter(type="tartes")
    venoiserie = Produits.objects.filter(type="venoiserie")
    confisserie = Produits.objects.filter(type="confisserie")
    snack = Produits.objects.filter(type="snack")
    gat_trad=Produits.objects.filter(type="gateau_trad")
    commande_livré=Commande.objects.filter(livré=True)
    commande_nonlivré=Commande.objects.filter(livré=False)
    actualites=News.objects.order_by("-id")
    context = {
        "Salé": Salé,
        "gateaux": gateaux,
        "glaces": glaces,
        "tartes": tartes,
        "venoiserie": venoiserie,
        "confisserie": confisserie,
        "snack": snack,  
        "gat_trad":gat_trad,
        "commande_livré":commande_livré,
        "actualites":actualites,
        "commande_nonlivré":commande_nonlivré
    }
    return render(request, "theme/admine.html", context)


def confisserie(request):
    conf = Produits.objects.filter(type="confisserie")
    context = {
        "conf": conf,  
    }
    return render(request, "theme/produits.html", context)


def gateaux(request):
    gat = Produits.objects.filter(type="gateaux")
    context = {
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def gateaux_trad(request):
    gat = Produits.objects.filter(type="gateau_trad")
    context = {
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def glace(request):
    gat = Produits.objects.filter(type="glaces")
    context = {
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def snack(request):
    gat = Produits.objects.filter(type="snack")
    context = {
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def venoiserie(request):
    gat = Produits.objects.filter(type="venoiserie")
    context = {
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def Salés(request):
    gat = Produits.objects.filter(type="salé")
    context = {
        
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

def Broc(request):
    gat = Produits.objects.filter(type="tartes")
    context = {
        
        "gat": gat,  
    }
    return render(request, "theme/produits.html", context)

@login_required
def commander(request,pr_id):
    produit = get_object_or_404(Produits, id=pr_id)
    context = {
        "produit":produit,
    }
    return render(request,"theme/commander.html",context)


def passer_commande(request, produit_id):
    if request.method == 'POST':
        produit = Produits.objects.get(id=produit_id)
        client = request.user
        quantite = int(request.POST['quantite'])
        methode_paiement = request.POST['payment-method']
        total_prix = quantite * produit.prix
        if methode_paiement == 'especes':
        # Créer une commande
            commande = Commande.objects.create(
                produit=produit,
                Client=client,
                methode_paiement=methode_paiement,
                payé=False,  # Mettre à jour selon votre logique de paiement
                prix=total_prix,
                Quantité=quantite
            )
        else:
            commande_pan=Commande_Panier.objects.create(
                produit=produit,
                Client=client,
                prix=total_prix,
                Quantité=quantite
            )
            return redirect('len:paiement', commande_id=commande_pan.id)
        # Rediriger ou effectuer une autre action
    return redirect('len:index')  
    


def paiement(request,commande_id):
    commande=get_object_or_404(Commande_Panier,id=commande_id)
    context={
        "commande":commande
    }
    return render(request,"theme/paiement.html",context)

    
@csrf_exempt
def payment_success(request, commande_id):
    if request.method == 'POST':
        order_id = request.POST.get('orderID')
        payer_id = request.POST.get('payerID')
        transaction_details = request.POST.get('transactionDetails')
        

        try:
            transaction_details = json.loads(transaction_details)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid transaction details'}, status=400)

        # Obtenez la réservation et créez ou mettez à jour Biens_Reservations
        commande_pan=get_object_or_404(Commande_Panier,id=commande_id)
        commande=Commande.objects.create(
            Client=commande_pan.Client,
            produit=commande_pan.produit,
            prix=commande_pan.prix,
            methode_paiement="en ligne",
            payé=True,
            libellé=f"""
            transaction_id: {order_id}
            transaction_date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            montant_payé: {commande_pan.prix}
            service_paiement: PayPal
            email_paiement: {transaction_details.get('payer', {}).get('email_address', 'N/A')}
        """
        )
        commande.save()
        commande_pan.delete()
        # Redirection vers le template success.html
        return render(request, 'theme/success.html ', {'commande_id': commande.id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



@login_required
def ajouter_Salé(request):
    if request.method == 'POST':
        form = AddSaléForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'salé'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddSaléForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_Gateau(request):
    if request.method == 'POST':
        form = AddGateauForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'gateaux'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddGateauForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_GateauTradit(request):
    if request.method == 'POST':
        form = AddGateauTraditionnelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'gateau_trad'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddGateauTraditionnelForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_tarte(request):
    if request.method == 'POST':
        form = AddtartesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'tartes'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddtartesForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_venoiserie(request):
    if request.method == 'POST':
        form = AddvenoiserieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'venoiserie'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddvenoiserieForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_conf(request):
    if request.method == 'POST':
        form = AddconfisserieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'confisserie'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddconfisserieForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_snack(request):
    if request.method == 'POST':
        form = AddsnackForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'snack'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddsnackForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})

@login_required
def ajouter_glace(request):
    if request.method == 'POST':
        form = AddglacesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                produit = form.save(commit=False)
                produit.type = 'glaces'
                produit.save()
                messages.success(request, 'Votre produit a été créé avec succès !')
                return redirect('len:admine')
            except IntegrityError:
                form.add_error(None, 'Une erreur s\'est produite lors de la création du produit. Veuillez réessayer.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AddglacesForm()  # Instantiation correcte du formulaire
    
    return render(request, 'theme/ajouter_salé.html', {'form': form})


@login_required
def modifier_salé(request, sl_id):
    salé = get_object_or_404(Produits, id=sl_id)
    
    if request.method == 'POST':
        form = SaléForm(request.POST, request.FILES, instance=salé)
        if form.is_valid():
            form.save()
            return redirect('len:admine')  # Replace with the name of the page you want to redirect to after modification
    else:
        form = SaléForm(instance=salé)

    return render(request, 'theme/modifier_salé.html', {'form': form, 'salé': salé})

@login_required
def annuler_produit(request, pr_id):
    produit_supp = get_object_or_404(Produits, id=pr_id)
    
    if request.method == 'POST':
        produit_supp.delete()
        return redirect(request.META.get('HTTP_REFERER', 'len:admine'))
    else:
        return redirect('len:admine') 
    
@login_required
def annuler_commande(request, pr_id):
    produit_supp = get_object_or_404(Commande, id=pr_id)
    
    if request.method == 'POST':
        produit_supp.delete()
        return redirect(request.META.get('HTTP_REFERER', 'len:admine'))
    else:
        return redirect('len:admine') 
    
@login_required
def livrer(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    
    
    commande.livré= True
    commande.payé=True
    commande.save()
    return redirect(request.META.get('HTTP_REFERER', 'len:admine'))
    
        
    

def generate_pdf(request, commande_id):
    # Récupérer les détails de la réservation
    commande = Commande.objects.get(id=commande_id)
    

    

    # Créer un buffer pour stocker le PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    

    # Définir les styles de texte
    c.setFont('Helvetica-Bold', 16)
    
    # Centrer le titre au-dessus de l'image
    title = "Reçu de Paiement"
    title_width = c.stringWidth(title, 'Helvetica-Bold', 16)
    c.drawString((width - title_width) / 2, height - 50, title)

    # Infos Client
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 100, "Informations du Client")
    c.setFont('Helvetica', 10)
    c.drawString(100, height - 120, f"Nom : {commande.Client.Nom}")
    c.drawString(100, height - 140, f"Prénom : {commande.Client.prenom}")

    # Infos Réservation
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, height - 180, "Détails de la Commande")
    c.setFont('Helvetica', 10)
    c.drawString(100, height - 200, f"Type de réservation : {commande.produit.Nom}")
    c.drawString(100, height - 220, f"Prix : {commande.prix} MAD")
    c.drawString(100, height - 240, f"Date de la commande : {commande.date_de_commande.strftime('%d/%m/%Y')}")
    c.drawString(100, height - 280, f"Durée : {commande.Quantité} ")

    
    

    # Infos Paiement
    c.setFont('Helvetica-Bold', 12)
    y_position = height - 440
    c.drawString(100, y_position, "Informations de Paiement")
    
    # Séparer les informations de paiement avec des lignes
    c.setFont('Helvetica', 10)
    y_position -= 20
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(100, y_position, width - 100, y_position)

    # Afficher les informations de paiement ligne par ligne
    if commande.libellé:
        for line in commande.libellé.splitlines():
            y_position -= 20
            c.drawString(100, y_position, line)
    else:
        y_position -= 20
        c.drawString(100, y_position, "Aucune information de paiement disponible.")

    # Ajouter le paragraphe de remerciement
    c.setFont('Helvetica', 10)
    y_position -= 40
    c.drawString(100, y_position, "Merci pour votre commande. Cette commande est uniquement disponible pour le retrait Pick-Up. Aucun service de livraison n'est proposé pour cette commande.")

    # Finaliser le PDF
    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recu_paiement_{commande_id}.pdf"'
    return response