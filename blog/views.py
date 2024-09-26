from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.template.defaultfilters import slugify

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, get_user_model

from .models import Posts
from .forms import AddPostForm, UserCreateForm, CustomPasswordChangeForm, ProfileSettingsForm

from transliterate import translit


class FeedView(ListView):
    paginate_by = 5
    template_name = 'blog/feed_page.html'

    def get_queryset(self):
        return Posts.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_ends=1)
        return context


class PostsView(LoginRequiredMixin, FeedView):
    template_name = 'blog/user_posts.html'

    def get_queryset(self):
        self.user_obj = get_object_or_404(User, username=self.kwargs['username'])
        return Posts.objects.filter(user=self.user_obj)


class PostDetailView(DetailView):
    model = Posts


class AddPostView(LoginRequiredMixin, CreateView):
    template_name = 'blog/add_post.html'
    form_class = AddPostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(translit(form.cleaned_data['title'], reversed=True))
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Posts
    form_class = AddPostForm
    template_name = 'blog/update_post.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Posts
    template_name = 'blog/delete_post.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'back' in request.POST:
            return redirect(reverse('blog:post_detail', kwargs={"slug": self.get_object().slug}))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:posts_list', kwargs={"username": self.request.user.username})

# Auth views

def registration_view(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('blog:posts_list', username=request.user.username)
    else:
        form = UserCreateForm()
    return render(request, 'registration/reg_page.html', {"form": form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("blog:password_change_done")


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileSettingsForm
    template_name = 'blog/profile_settings.html'

    def get_success_url(self):
        return reverse_lazy("blog:posts_list", self.request.user.username)

    def get_object(self, queryset=None):
        return self.request.user