# Generated by Django 2.0 on 2017-12-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctree', '0004_auto_20171218_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
