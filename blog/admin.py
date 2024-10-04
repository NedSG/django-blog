from django.contrib import admin

from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ['author', 'text', 'date_created', 'parent_comment']
    readonly_fields = ['date_created']


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'author', 'slug']}),
        ("Content", {"fields": ['content']}),
    ]
    inlines = [CommentInline]
    list_display = ['title', 'author', 'date_created', 'last_modified']
    list_filter = ['author', 'date_created']
    search_fields = ['author', 'date_created']
    list_per_page = 10


admin.AdminSite.site_header = "Панель администрирования"
admin.AdminSite.site_index = "Блог"
admin.site.register(Post, PostAdmin)
