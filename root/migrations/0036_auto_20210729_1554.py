# Generated by Django 2.2.13 on 2021-07-29 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0035_auto_20210729_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattracker',
            name='iehBool',
            field=models.BooleanField(default=True),
        ),
    ]