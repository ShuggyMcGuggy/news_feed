# Generated by Django 3.2.6 on 2022-01-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0004_auto_20220115_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='source_name',
            field=models.CharField(default=' ', max_length=100),
        ),
    ]