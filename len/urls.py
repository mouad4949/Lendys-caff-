from django.urls import path,include
from . import views

app_name = 'len'

urlpatterns = [
     path("", views.index, name="index"),

     path('login/', views.login_view, name='login'),
     path('register/', views.Register_view, name='register'),
     path('logout/', views.logout_view, name='logout'),
     path('admine/', views.admine, name='admine'),
     path('conf/', views.confisserie, name='conf'),
     path('gat/', views.gateaux, name='gat'),
     path('gat_trad/', views.gateaux_trad, name='gat_trad'),
     path('glace/', views.glace, name='glace'),
     path('snack/', views.snack, name='snack'),
     path('venoiserie/', views.venoiserie, name='venoiserie'),
     path('Salés/', views.Salés, name='Salés'),
     path('Broc/', views.Broc, name='Broc'),
     path('commander/<int:pr_id>', views.commander, name='commander'),
     path('passer_commande/<int:produit_id>', views.passer_commande, name='passer_commande'),
     path('paiement/<int:commande_id>', views.paiement, name='paiement'),
     path('paiement_success/<int:commande_id>', views.payment_success, name='paiement_success'),
     path('recu/<int:commande_id>', views.generate_pdf, name='download_receipt'),
     path('ajouter_salé/', views.ajouter_Salé, name='ajouter_salé'),
     path('ajouter_gateau/', views.ajouter_Gateau, name='ajouter_gateau'),
     path('ajouter_gateau_trad/', views.ajouter_GateauTradit, name='ajouter_gateau_trad'),
     path('ajouter_tarte/', views.ajouter_tarte, name='ajouter_tarte'),
     path('ajouter_snack/', views.ajouter_snack, name='ajouter_snack'),
     path('ajouter_conf/', views.ajouter_conf, name='ajouter_conf'),
     path('ajouter_glace/', views.ajouter_glace, name='ajouter_glace'),
     path('ajouter_venoiserie/', views.ajouter_venoiserie, name='ajouter_venoiserie'),
     path('modifier_salé/<int:sl_id>', views.modifier_salé, name='modifier_salé'),
     path('annuler_produit/<int:pr_id>', views.annuler_produit, name='annuler_produit'),
     path('annuler_commande/<int:pr_id>', views.annuler_commande, name='annuler_commande'),
     path('livré/<int:commande_id>/', views.livrer, name='livrer'),
]