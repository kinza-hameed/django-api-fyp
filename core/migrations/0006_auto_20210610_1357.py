# Generated by Django 3.1.2 on 2021-06-10 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210610_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicaltestrecord',
            name='result',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
    ]