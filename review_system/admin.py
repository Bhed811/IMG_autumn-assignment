from django.contrib import admin
from .models import User, Role, Team, Assignment, Submission, Subtask, Review, ReviewComment, Attachment

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Team)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Subtask)
admin.site.register(Review)
admin.site.register(ReviewComment)
admin.site.register(Attachment)
