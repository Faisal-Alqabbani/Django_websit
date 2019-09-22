from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('ajax/validation_username/', views.validation_username, name='validation_username'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my_account/', views.profiles, name='my_account'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Password-reset-done.html'), name='password_reset_done'),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name='password-reset-confirm.html'
                       ),
                       name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset-complete.html'
         ),
         name='password_reset_complete'),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             template_name='password-change.html'
         ),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordResetDoneView.as_view(template_name='Password-change-done.html'), name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)