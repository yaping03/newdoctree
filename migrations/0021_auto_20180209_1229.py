# Generated by Django 2.0.1 on 2018-02-09 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctree', '0020_auto_20180209_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celebrity',
            name='avatar',
            field=models.ImageField(default='upload/avatar/defult.jpg', upload_to='upload/avatar', verbose_name='头像'),
        ),
    ]
