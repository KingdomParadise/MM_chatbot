# Generated by Django 2.2.13 on 2021-09-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_auto_20210902_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattracker',
            name='iehBool',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
