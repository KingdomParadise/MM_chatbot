# Generated by Django 2.2.13 on 2021-07-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0033_chattracker_eligibiltyprograms'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattracker',
            name='variable_state',
            field=models.CharField(blank=True, default='', max_length=5000),
        ),
    ]