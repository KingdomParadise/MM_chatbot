# Generated by Django 2.2.13 on 2021-07-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0037_auto_20210730_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattracker',
            name='iehBool',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='chattracker',
            name='token',
            field=models.CharField(default='d3a1b634-90a7-eb11-a963-005056a96ce9', max_length=40),
        ),
    ]