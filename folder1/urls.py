from django.urls import path, re_path, include
from users import views
from django.conf import settings
from django.conf.urls.static import static
from users import forms
from django.contrib.auth import views as auth_views



urlpatterns = [    
    path('profile', views.profile, name='profile'),
    path('image-update', views.imageUpdate, name='image-update'),
    path('change-password', views.change_password, name='change-password'),
    path('', include('django.contrib.auth.urls')),
    path('password-reset/', auth_views.PasswordResetView.as_view(
    path('add_user', views.add_user, name='add_user'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user')
        gfgf
        ffgdfd
]
