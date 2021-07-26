# Generated by Django 2.2.13 on 2021-07-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0028_merge_20210720_1603'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StartOrder',
        ),
        migrations.DeleteModel(
            name='UserConfiguration',
        ),
        migrations.AddField(
            model_name='chattracker',
            name='OrderNumber',
            field=models.CharField(blank=True, default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='PackageID',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='TribalResident',
            field=models.NullBooleanField(default=False),
        ),
    ]