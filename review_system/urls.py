from django.urls import path
from .views import SignUpView, LoginView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/channeli/', views.RequestAccessAPI.as_view(), name='login-channeli'),
    path('home/', views.HelloWorldView.as_view(), name='home'),
]
