# Generated by Django 5.0.2 on 2024-04-01 03:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0006_anolectivo_rename_tema_desempeno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colegio',
            fields=[
                ('codigo_colegio', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('nombre_colegio', models.CharField(max_length=60)),
                ('razonsocial_colegio', models.CharField(max_length=35)),
                ('direccion_colegio', models.CharField(max_length=35)),
                ('telefono_colegio', models.CharField(max_length=35)),
                ('email_colegio', models.CharField(max_length=100)),
                ('tipo_colegio', models.CharField(choices=[('A', 'Publico'), ('B', 'Privado')], default='A', max_length=1)),
                ('calendario_colegio', models.CharField(choices=[('A', 'Calendario A'), ('B', 'Calendario B')], default='A', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='anolectivo',
            name='colegio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Academico.colegio'),
        ),
    ]
