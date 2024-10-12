# Generated by Django 5.1.1 on 2024-10-06 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarium_main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='name',
            field=models.CharField(choices=[('Inicial', 'Inicial'), ('Primera', 'Primera'), ('Segunda', 'Segunda'), ('Tercera', 'Tercera')], max_length=100),
        ),
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.CharField(choices=[('Insuficiente', 'Insuficiente'), ('Suficiente', 'Suficiente'), ('Bien', 'Bien'), ('Notable', 'Notable'), ('Sobresaliente', 'Sobresaliente')], max_length=20),
        ),
    ]