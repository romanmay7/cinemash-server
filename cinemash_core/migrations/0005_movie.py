# Generated by Django 4.0 on 2024-02-27 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemash_core', '0004_alter_genericmoviedata_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tmdb_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('original_title', models.CharField(max_length=255)),
                ('original_language', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('adult', models.BooleanField(default=True)),
                ('backdrop_path', models.URLField()),
                ('genre_ids', models.TextField(blank=True)),
                ('popularity', models.IntegerField()),
                ('poster_path', models.URLField()),
                ('release_date', models.CharField(max_length=255)),
                ('video', models.BooleanField(default=True)),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
            ],
        ),
    ]
