from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import Posts
from .forms import AddPostForm

class PostsView(ListView):
    queryset = Posts.objects.order_by('-date_created')
    template_name = 'blog/posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_ends=1)
        return context


class PostDetailView(DetailView):
    model = Posts


class AddPostView(CreateView):
    template_name = 'blog/add_post.html'
    form_class = AddPostForm


class UpdatePostView(UpdateView):
    model = Posts
    form_class = AddPostForm
    template_name = 'blog/update_post.html'


class DeletePostView(DeleteView):
    model = Posts
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:posts_list')

    def post(self, request, *args, **kwargs):
        if 'back' in request.POST:
            return redirect(reverse('blog:post_detail', kwargs={"pk": self.get_object().pk}))
        return super().post(request, *args, **kwargs)