# Generated by Django 3.0.6 on 2020-10-06 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0009_auto_20200926_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockrecord',
            name='remark',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]