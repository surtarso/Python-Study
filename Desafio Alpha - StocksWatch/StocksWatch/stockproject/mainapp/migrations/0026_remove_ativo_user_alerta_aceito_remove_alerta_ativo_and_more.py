# Generated by Django 4.0.5 on 2022-06-18 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_remove_alerta_ativo_alerta_ativo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativo',
            name='user',
        ),
        migrations.AddField(
            model_name='alerta',
            name='aceito',
            field=models.BooleanField(default=True),
        ),
        migrations.RemoveField(
            model_name='alerta',
            name='ativo',
        ),
        migrations.AddField(
            model_name='alerta',
            name='ativo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.ativo'),
        ),
        migrations.AlterField(
            model_name='alerta',
            name='email',
            field=models.EmailField(default='fill@me.plz', max_length=254),
        ),
    ]