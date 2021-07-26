# Generated by Django 2.2.13 on 2021-07-21 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0029_auto_20210721_1123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chattracker',
            old_name='PackageID',
            new_name='PackageId',
        ),
        migrations.AddField(
            model_name='chattracker',
            name='FcraAcknowledgement',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='FcraAdditionalDisclosureText',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='FcraDisclosureText',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='ReservationAgentCode',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
