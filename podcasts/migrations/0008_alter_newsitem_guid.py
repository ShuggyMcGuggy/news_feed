# Generated by Django 3.2.6 on 2022-03-15 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0007_newsitem_star_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='guid',
            field=models.CharField(max_length=200),
        ),
    ]
