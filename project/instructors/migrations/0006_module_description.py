# Generated by Django 4.0.5 on 2023-09-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0005_catagory_course_published_course_catagory'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='description',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
