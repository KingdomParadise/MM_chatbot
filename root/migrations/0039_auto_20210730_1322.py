# Generated by Django 2.2.13 on 2021-07-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0038_auto_20210730_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattracker',
            name='iehBool',
            field=models.BooleanField(default=False),
        ),
    ]