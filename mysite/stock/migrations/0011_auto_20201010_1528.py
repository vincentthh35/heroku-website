# Generated by Django 3.0.6 on 2020-10-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_stockrecord_remark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockrecord',
            name='remark',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
