# Generated by Django 3.2.4 on 2021-07-19 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0025_auto_20210719_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattracker',
            name='residency_nature',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]