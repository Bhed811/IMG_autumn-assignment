from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
# Unregister the existing User model if it has been registered before
admin.site.unregister(User)  # Comment this line if your custom User model has not been registered yet

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'second_name', 'is_staff', 'is_active')  # Add your fields here

# Register the User model with the CustomUserAdmin class
admin.site.register(User, CustomUserAdmin)