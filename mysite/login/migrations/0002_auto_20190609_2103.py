# Generated by Django 2.2.1 on 2019-06-09 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_name',
            field=models.CharField(max_length=100, verbose_name='姓名'),
        ),
    ]
