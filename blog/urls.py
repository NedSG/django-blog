from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from . import views
from .forms import CustomAuthenticationForm

app_name = 'blog'

posts_patterns = [
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('delete/<slug:slug>/', views.DeletePostView.as_view(), name='delete_post'),
    path('update/<slug:slug>/', views.UpdatePostView.as_view(), name='update_post'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

account_patterns = [
    path('login/', auth_views.LoginView.as_view(
        form_class=CustomAuthenticationForm,
        redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_success_page.html'),
         name='password_change_done'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password-reset-form.html',
             email_template_name='registration/password-reset-email.html',
             success_url=reverse_lazy("blog:password_reset_done")),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password-reset-done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password-reset-confirm.html',
             success_url=reverse_lazy("blog:password_reset_complete")),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password-reset-complete.html'),
         name='password_reset_complete'),
]

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('blog:feed_page'))),
    path('profile/settings/', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('profile/<username>/', views.PostsView.as_view(), name='posts_list'),
    path('posts/', include(posts_patterns)),
    path('accounts/', include(account_patterns)),
    path('feed/', views.FeedView.as_view(), name='feed_page'),
]
