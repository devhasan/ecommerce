from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/', views.user_profile, name='user_profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('newpassword/<uidb64>/<token>/', views.newpassword, name='newpassword'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('email_change_verification/', views.email_change_verification, name='email_change_verification'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    # path('user_update/', views.user_update, name='user_update'),
]