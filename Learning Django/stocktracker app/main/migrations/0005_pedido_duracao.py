# Generated by Django 4.0.5 on 2022-06-15 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_pedido_checkbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='duracao',
            field=models.DateField(default=datetime.date.today),
        ),
    ]