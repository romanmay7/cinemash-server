# Generated by Django 4.0 on 2024-02-29 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('cinemash_core', '0005_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('location', models.TextField()),
                ('favorite_genres_ids', models.TextField(blank=True)),
                ('age', models.IntegerField()),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='auth.user')),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
