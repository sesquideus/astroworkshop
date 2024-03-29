# Generated by Django 3.1.7 on 2021-02-28 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20210228_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='note',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='slot',
            name='abstract',
            field=models.TextField(blank=True, default='', max_length=4096),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='slot',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='slot',
            name='title',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
    ]
