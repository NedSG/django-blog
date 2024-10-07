from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from transliterate import translit

from .forms import AddPostForm, UserCreateForm, CustomPasswordChangeForm, ProfileSettingsForm, AddCommentForm
from .models import Post, Comment


class FeedView(ListView):
    """
    Представление для списка постов на общей странице постов.

    Это class-based view, который возвращает список постов всех пользователей и рендереит HTML-страницу.

    Template:
        - `blog/feed_page.html`.

    Model:
        - `Post`

    Attributes:
        - paginate_by (int): Кол-во записей на одну страницу.
        - template_name (str): Имя шаблона, используемого для отобрежния списка постов.

    Context:
        - paginator_range (list): Список отображаемых страниц для выбора в зависимости от страницы.
    """
    paginate_by = 5
    template_name = 'blog/feed_page.html'

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_ends=1)
        return context


class PostsView(FeedView):
    """
    Представление для постов отдельного пользователя.

    Это class-based view который возвращает список постов отдельного пользователя и рендереит HTML-страницу.
    Наследуется от `FeedView`.

    Template:
        - `blog/user_posts.html`.

    Model:
        - `Post`.

    Attributes:
        - template_name (str): Имя шаблона, используемого для отобрежния списка постов.
    """
    template_name = 'blog/user_posts.html'

    def get_queryset(self):
        self.user_obj = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(author=self.user_obj)


class PostDetailView(DetailView):
    """
    Представление для отображения поста.

    Это class-based view который возвращает отдельный пост с комментариями и рендерит HTML-страницу.

    Template:
        - `blog/post_detail.html`.

    Model:
        - `Post`, `Comment`.

    Form:
        - `AddCommentForm`

    Attributes:
        - model (Post): используемая модель.
        - context_object_name (str): Имя объекта `Post` используемое в шаблоне.

    Context:
        - comments_tree (list): Возвращает список словарей со всеми комментариями и их дочерними комментариями.
        - form (AddCommentForm): Форма для создания комментария.
    """
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.prefetch_related('child_comments')
        context['comments_tree'] = Comment.make_recursive_comments_list(comments)
        context['form'] = AddCommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', slug=self.object.slug)
        return render(request, self.template_name, self.get_context_data(form=form))


class AddPostView(LoginRequiredMixin, CreateView):
    """
    Представление для создания поста.

    Это class-based view для создания поста. Отображает форму, проверяет, чтобы пост мог создать только
    зарегестрированный пользователь и создаёт запись в модели Post.

    Template:
        - `blog/add_post.html`.

    Model:
        - `Post`.

    Form:
        - `AddPostForm`.

    Attributes:
        - template_name (str): Имя используемого шаблона.
        - form_class (AddPostForm): Используемая форма.
    """
    template_name = 'blog/add_post.html'
    form_class = AddPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(translit(form.cleaned_data['title'], reversed=True))
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Представление для изменения поста.

    Это class-based view для изменения поста. Отображает форму; проверяет, чтобы пост мог изменить только
    зарегестрированный пользователь и пользователь мог изменять только свои посты; обновляет запись в модели Post.

    Template:
        - `blog/update_post.html`.

    Model:
        - `Post`.

    Form:
        - `AddPostForm`.

    Attributes:
        - model (Post): Используемая модель.
        - form_class (AddPostForm): Используемая форма.
        - template_name (str): Имя используемого шаблона.
    """
    model = Post
    form_class = AddPostForm
    template_name = 'blog/update_post.html'

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)


class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления поста.

    Это class-based view для удаления поста. Проверяет, чтобы пост мог удалять только
    зарегестрированный пользователь и пользователь мог удалять только свои посты;
    отображает страницу подтверждения удаления; удаляет запись в модели Post.

    Template:
        - `blog/delete_post.html`.

    Model:
        - `Post`.

    Attributes:
        - model (Post): Используемая модель.
        - template_name (str): Имя используемого шаблона.
    """
    model = Post
    template_name = 'blog/delete_post.html'

    def get(self, request, *args, **kwargs):
        """Проверяет, что пост принадлежит пользователю."""
        if request.user != self.get_object().author:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Добавляет возможность вернуться на страницу отображения поста."""
        if 'back' in request.POST:
            return redirect(reverse('blog:post_detail', kwargs={"slug": self.get_object().slug}))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:posts_list', kwargs={"username": self.request.user.username})


# Auth views

def registration_view(request):
    """
    Представление для регистрации пользователя.

    Отображает форму для регистрации, и в случае успешной регистрации реализует вход в систему и
    перенаправляет на страницу постов пользователя.

    Template:
        - `registration\reg_page.html`.

    Model:
        - `User`.

    Form:
        - `UserCreateForm`

    Context:
        - form (UserCreateForm): форма регистрации.
    """
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('blog:posts_list', username=request.user.username)
    else:
        form = UserCreateForm()
    return render(request, 'registration/reg_page.html', {"form": form})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Представление для смены пароля пользователя.

    Позволяет пользователю менять пароль. Отображает страницу с формой для смены пароля.

    Template:
        - `registration/password_change.html`.

    Model:
        - `User`.

    Attributes:
        - template_name (str): Имя используемого шаблона.
        - form_class (CustomPasswordChangeForm): Используемая форма.
        - success_url (HttpResponse): Страница перенаправления, в случае успеха.
    """
    template_name = 'registration/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("blog:password_change_done")


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    """
    Представление для изменения данных о пользователе.

    Позволяет пользователю задать имя, фамилию, и перейти на страницу изменения пароля.

    Template:
        - `blog/profile_settings.html`.

    Model:
        - `User`.

    Attributes:
        - model (User):
        - form_class (ProfileSettingsForm): Используемая форма.
        - template_name (str): Имя используемого шаблона.
    """
    model = get_user_model()
    form_class = ProfileSettingsForm
    template_name = 'blog/profile_settings.html'

    def get_success_url(self):
        return reverse_lazy("blog:posts_list", args=(self.request.user.username,))

    def get_object(self, queryset=None):
        return self.request.user
