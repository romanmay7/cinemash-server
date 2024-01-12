# Generated by Django 4.0 on 2024-01-12 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenericMovieData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('genre', models.CharField(max_length=50)),
                ('release_date', models.DateTimeField(auto_now=True)),
                ('poster_url', models.URLField(max_length=150)),
            ],
        ),
    ]
