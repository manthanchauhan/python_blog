# Generated by Django 2.2.1 on 2019-05-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20190511_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='description',
            field=models.CharField(max_length=100),
        ),
    ]


