# Generated by Django 3.2.4 on 2021-06-25 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0018_auto_20210625_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chattracker',
            name='replyforbestway',
        ),
        migrations.RemoveField(
            model_name='chattracker',
            name='replyforfourdigitpin',
        ),
        migrations.RemoveField(
            model_name='chattracker',
            name='replyforphonenumber',
        ),
    ]