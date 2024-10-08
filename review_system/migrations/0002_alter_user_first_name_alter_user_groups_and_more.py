# Generated by Django 5.1 on 2024-10-08 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('review_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='users', to='review_system.role'),
        ),
        migrations.AlterField(
            model_name='user',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='members', to='review_system.team'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission'),
        ),
    ]
