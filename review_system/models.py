from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class Role(models.Model):
    ROLE_CHOICES = [
        ('reviewer', 'Reviewer'),
        ('reviewee', 'Reviewee'),
        ('admin', 'Admin'),
    ]

    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    second_name = models.CharField(max_length=50)
    
    # Remove first_name as it already exists in AbstractUser
    # If you want to keep first_name as is, you can just customize it:
    # first_name = models.CharField(max_length=50)  # Not necessary, already exists in AbstractUser

    # ManyToMany fields that clash with auth.User are assigned a related_name
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    roles = models.ManyToManyField('Role', related_name='users', blank=True)
    teams = models.ManyToManyField('Team', related_name='members', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    class Meta:
        ordering = ['first_name', 'second_name']


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.team_name


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_date = models.DateTimeField(auto_now_add=True)

    # ForeignKey to User (created_by)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_assignments')

    # Many-to-Many relationship for individual reviewees (Users)
    individual_reviewees = models.ManyToManyField('User', related_name='assignments_as_individual')

    # Many-to-Many relationship for team reviewees (Teams)
    team_reviewees = models.ManyToManyField(Team, related_name='assignments_as_team')

    def __str__(self):
        return self.title


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    submission_description = models.TextField()
    files_link = models.URLField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # ForeignKey to Subtask
    subtask = models.ForeignKey('Subtask', on_delete=models.CASCADE, related_name='submissions')

    # ForeignKey to User (reviewee)
    reviewee = models.ForeignKey('User', on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return f"Submission {self.submission_id} by {self.reviewee}"


class Subtask(models.Model):
    subtask_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()

    # Foreign Key to Assignment
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_content = models.TextField()
    additional_comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    # Status as an Enum field (choices in Django)
    STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('suggest_iteration', 'Suggest Iteration'),  # updated to be more consistent with enum-like convention
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # Foreign Keys
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review {self.review_id} - {self.status}"


class ReviewComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    # Foreign Keys
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey('User', on_delete=models.CASCADE, related_name='review_comments')

    def __str__(self):
        return f"Comment {self.comment_id} on Review {self.review.review_id}"


class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    submission = models.ForeignKey('Submission', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    subtask = models.ForeignKey('Subtask', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)

    def clean(self):
        super().clean()
        if not (self.submission or self.review or self.subtask):
            raise ValidationError("Attachment must be associated with at least one of Submission, Review, or Subtask.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attachment {self.attachment_id} uploaded at {self.uploaded_at}"

