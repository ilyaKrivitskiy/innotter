# Generated by Django 4.2.3 on 2023-08-04 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]