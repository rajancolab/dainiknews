# Generated by Django 3.1.2 on 2020-10-31 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20201031_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
