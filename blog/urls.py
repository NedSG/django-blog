from django.urls import path, include
from django.contrib.auth import views as auth_views

from blog import views
from .forms import CustomAuthenticationForm


app_name = 'blog'

posts_patterns = [
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update_post'),
    path('<username>', views.PostsView.as_view(), name='posts_list'),
]

account_patterns = [
    path('login/', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registration/', views.registration_view, name='registration'),
]


urlpatterns = [
    path('posts/', include(posts_patterns)),
    path('accounts/', include(account_patterns)),
    path('feed/', views.FeedView.as_view(), name='feed_page'),
]
