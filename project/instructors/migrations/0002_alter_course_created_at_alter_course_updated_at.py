# Generated by Django 4.2.4 on 2023-09-26 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
