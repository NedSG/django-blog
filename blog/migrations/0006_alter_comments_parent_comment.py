# Generated by Django 5.1.1 on 2024-09-27 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_user_posts_author_alter_posts_slug_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comments'),
        ),
    ]
