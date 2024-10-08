# Generated by Django 5.1 on 2024-10-05 06:33

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(choices=[('reviewer', 'Reviewer'), ('reviewee', 'Reviewee'), ('admin', 'Admin')], max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('submission_id', models.AutoField(primary_key=True, serialize=False)),
                ('submission_description', models.TextField()),
                ('files_link', models.URLField(max_length=500)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_content', models.TextField()),
                ('additional_comments', models.TextField(blank=True, null=True)),
                ('reviewed_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('passed', 'Passed'), ('suggest_iteration', 'Suggest Iteration')], max_length=20)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='review_system.submission')),
            ],
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('subtask_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='review_system.assignment')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='subtask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='review_system.subtask'),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='attachments/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='review_system.review')),
                ('submission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='review_system.submission')),
                ('subtask', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='review_system.subtask')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='team_reviewees',
            field=models.ManyToManyField(related_name='assignments_as_team', to='review_system.team'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(related_name='custom_user_set', to='auth.group')),
                ('roles', models.ManyToManyField(related_name='users', to='review_system.role')),
                ('teams', models.ManyToManyField(related_name='members', to='review_system.team')),
                ('user_permissions', models.ManyToManyField(related_name='custom_user_permissions', to='auth.permission')),
            ],
            options={
                'ordering': ['first_name', 'second_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='reviewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='review_system.user'),
        ),
        migrations.CreateModel(
            name='ReviewComment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='review_system.review')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='review_system.user')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='review_system.user'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_assignments', to='review_system.user'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='individual_reviewees',
            field=models.ManyToManyField(related_name='assignments_as_individual', to='review_system.user'),
        ),
    ]
