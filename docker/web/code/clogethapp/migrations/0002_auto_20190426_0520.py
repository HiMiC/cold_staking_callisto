# Generated by Django 2.2 on 2019-04-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clogethapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='gasPrice',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
