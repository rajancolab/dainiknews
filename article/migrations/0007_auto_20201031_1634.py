# Generated by Django 3.1.2 on 2020-10-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20201031_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1000),
        ),
    ]
