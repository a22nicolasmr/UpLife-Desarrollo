# Generated by Django 4.2.20 on 2025-04-22 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UpLife_api', '0006_alter_usuarios_imaxe_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medallas',
            name='usuario',
        ),
        migrations.AddField(
            model_name='medallas',
            name='usuarios',
            field=models.ManyToManyField(to='UpLife_api.usuarios'),
        ),
    ]
