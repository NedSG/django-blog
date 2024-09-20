from django.urls import path
from django.views.generic.edit import FormView
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add/', views.AddPostView.as_view(), name='add_post'),
    path('delete/<int:pk>/', views.DeletePostView.as_view(), name='delete_post'),
    path('update/<int:pk>/', views.UpdatePostView.as_view(), name='update_post'),
]