from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Posts

class PostsView(ListView):
    queryset = Posts.objects.order_by('-date_created')
    template_name = 'blog/posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_ends=1)
        return context


class AddPostView(CreateView):
    template_name = 'blog/add_post.html'
    model = Posts
    fields = ['title', 'content']

class PostDetailView(DetailView):
    model = Posts