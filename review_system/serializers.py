from rest_framework import serializers
from .models import User, Role, Team, Assignment, Submission, Subtask, Review, ReviewComment, Attachment


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']




class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)  # Writable nested serializer for roles


    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'second_name', 'email', 'roles']


    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        user = User.objects.create(**validated_data)
        for role_data in roles_data:
            role, _ = Role.objects.get_or_create(**role_data)
            user.roles.add(role)
        return user


    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', [])
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.second_name = validated_data.get('second_name', instance.second_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()


        if roles_data:
            instance.roles.clear()  # Clear existing roles
            for role_data in roles_data:
                role, _ = Role.objects.get_or_create(**role_data)
                instance.roles.add(role)
        return instance




class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_id', 'team_name']




class AssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Use ID for user


    class Meta:
        model = Assignment
        fields = ['assignment_id', 'title', 'description', 'assigned_date', 'created_by']


    def create(self, validated_data):
        return Assignment.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()
        return instance




class SubtaskSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())  # Use ID for assignment


    class Meta:
        model = Subtask
        fields = ['subtask_id', 'title', 'description', 'due_date', 'assignment']


    def create(self, validated_data):
        return Subtask.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.assignment = validated_data.get('assignment', instance.assignment)
        instance.save()
        return instance




class SubmissionSerializer(serializers.ModelSerializer):
    subtask = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all())
    reviewee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = Submission
        fields = ['submission_id', 'submission_description', 'files_link', 'submitted_at', 'subtask', 'reviewee']


    def create(self, validated_data):
        return Submission.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.submission_description = validated_data.get('submission_description', instance.submission_description)
        instance.files_link = validated_data.get('files_link', instance.files_link)
        instance.subtask = validated_data.get('subtask', instance.subtask)
        instance.reviewee = validated_data.get('reviewee', instance.reviewee)
        instance.save()
        return instance




class ReviewSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())
    reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = Review
        fields = ['review_id', 'review_content', 'additional_comments', 'reviewed_at', 'status', 'submission', 'reviewer']


    def create(self, validated_data):
        return Review.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.review_content = validated_data.get('review_content', instance.review_content)
        instance.additional_comments = validated_data.get('additional_comments', instance.additional_comments)
        instance.status = validated_data.get('status', instance.status)
        instance.submission = validated_data.get('submission', instance.submission)
        instance.reviewer = validated_data.get('reviewer', instance.reviewer)
        instance.save()
        return instance




class ReviewCommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    commenter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    class Meta:
        model = ReviewComment
        fields = ['comment_id', 'comment', 'commented_at', 'review', 'commenter']


    def create(self, validated_data):
        return ReviewComment.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.review = validated_data.get('review', instance.review)
        instance.commenter = validated_data.get('commenter', instance.commenter)
        instance.save()
        return instance




class AttachmentSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all(), required=False)
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), required=False)
    subtask = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), required=False)


    class Meta:
        model = Attachment
        fields = ['attachment_id', 'file', 'uploaded_at', 'submission', 'review', 'subtask']


    def create(self, validated_data):
        return Attachment.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.file = validated_data.get('file', instance.file)
        instance.submission = validated_data.get('submission', instance.submission)
        instance.review = validated_data.get('review', instance.review)
        instance.subtask = validated_data.get('subtask', instance.subtask)
        instance.save()
        return instance
