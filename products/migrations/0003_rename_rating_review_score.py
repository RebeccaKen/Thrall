# Generated by Django 3.2.19 on 2023-07-21 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rating',
            new_name='score',
        ),
    ]
