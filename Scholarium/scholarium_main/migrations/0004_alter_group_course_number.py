# Generated by Django 5.1.1 on 2024-10-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarium_main', '0003_alter_schedule_day_of_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='course_number',
            field=models.CharField(max_length=10),
        ),
    ]