from django.urls import path
from django.views.generic.edit import FormView
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add/', views.AddPostView.as_view(), name='add_post'),
]