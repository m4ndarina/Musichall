# Generated by Django 5.0.4 on 2024-05-12 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0015_remove_desempeno_url_imagen_desempeno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='imagen_material',
            field=models.FileField(null=True, upload_to='material_imagen/', verbose_name='Imagen del material'),
        ),
    ]
