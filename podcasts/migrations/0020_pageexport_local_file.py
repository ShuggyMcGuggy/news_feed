# Generated by Django 3.2.6 on 2022-05-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0019_auto_20220501_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageexport',
            name='local_file',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
