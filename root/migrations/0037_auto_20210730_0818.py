# Generated by Django 2.2.13 on 2021-07-30 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0036_auto_20210729_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('sequence_id', models.CharField(max_length=18, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('type', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='chattracker',
            name='benefit_code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='sequence_count',
            field=models.CharField(default='0', max_length=5),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='token',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='zap_acct',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='chattracker',
            name='zap_name',
            field=models.CharField(default='', max_length=10),
        ),
    ]
