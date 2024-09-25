from django.urls import path, include
from django.contrib.auth import views as auth_views

from blog import views
from .forms import CustomAuthenticationForm


app_name = 'blog'

posts_patterns = [
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update_post'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

account_patterns = [
    path('login/', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm, redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path(
        'password-change-success/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_success_page.html'),
        name='password_change_success'),
    path('unauth/<username>/', views.deactivate_user_view, name='deactivate_user')
]


urlpatterns = [
    path('profile/<username>/', views.PostsView.as_view(), name='posts_list'),
    path('posts/', include(posts_patterns)),
    path('accounts/', include(account_patterns)),
    path('feed/', views.FeedView.as_view(), name='feed_page'),
]
