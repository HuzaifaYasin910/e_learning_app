# Generated by Django 4.2.4 on 2023-09-28 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0002_alter_course_created_at_alter_course_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='order',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
