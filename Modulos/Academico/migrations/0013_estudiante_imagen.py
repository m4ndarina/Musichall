# Generated by Django 5.0.2 on 2024-05-04 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0012_remove_curso_url_imagen_curso_curso_imagen_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='imagen',
            field=models.FileField(null=True, upload_to='imagen_estudiante/', verbose_name='Foto de perfil del estudiante'),
        ),
    ]
