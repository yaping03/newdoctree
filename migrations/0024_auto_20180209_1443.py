# Generated by Django 2.0.1 on 2018-02-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctree', '0023_auto_20180209_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='content',
            field=models.TextField(),
        ),
    ]
