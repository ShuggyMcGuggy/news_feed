# Generated by Django 3.2.6 on 2022-03-20 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0013_publication_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image_file',
            field=models.CharField(default='wip.jpeg', max_length=20),
        ),
    ]
