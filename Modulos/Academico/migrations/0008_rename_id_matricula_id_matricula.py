# Generated by Django 5.0.2 on 2024-04-17 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0007_colegio_anolectivo_colegio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matricula',
            old_name='id',
            new_name='id_matricula',
        ),
    ]
