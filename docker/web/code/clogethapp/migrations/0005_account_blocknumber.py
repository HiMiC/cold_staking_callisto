# Generated by Django 2.2 on 2019-04-29 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clogethapp', '0004_csbalance'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='blockNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
