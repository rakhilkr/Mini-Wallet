# Generated by Django 3.1.7 on 2022-10-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='enabled_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='withdrawn_at',
            field=models.DateTimeField(),
        ),
    ]
