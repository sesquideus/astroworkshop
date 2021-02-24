# Generated by Django 3.1.7 on 2021-02-24 14:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210224_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='person',
            field=models.ManyToManyField(blank=True, related_name='people', to=settings.AUTH_USER_MODEL),
        ),
    ]
