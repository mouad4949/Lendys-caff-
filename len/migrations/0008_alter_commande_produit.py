# Generated by Django 5.0.6 on 2024-09-01 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('len', '0007_alter_commande_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='len.produits'),
        ),
    ]
