# Generated by Django 4.2.20 on 2025-04-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UpLife_api', '0005_medallas_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='imaxe_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='avatares'),
        ),
    ]
