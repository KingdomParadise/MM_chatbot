# Generated by Django 2.2.13 on 2021-08-03 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0040_auto_20210731_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattracker',
            name='ApplicationStatus',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='Check_NVEligibility_url',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
