# Generated by Django 3.2.6 on 2022-05-01 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0017_publication_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageExport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('export_type', models.CharField(choices=[('Local', 'Local'), ('Dropbox', 'Dropbox'), ('FTP', 'FTP')], default='Local', max_length=512)),
                ('source_page_url', models.URLField(max_length=300)),
                ('target_page_url', models.URLField(max_length=300)),
                ('local_dir', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
