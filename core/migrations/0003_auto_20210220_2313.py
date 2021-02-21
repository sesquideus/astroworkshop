# Generated by Django 3.1.7 on 2021-02-20 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210220_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='name',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='surname',
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
