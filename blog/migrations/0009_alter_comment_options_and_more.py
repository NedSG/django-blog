# Generated by Django 5.1.1 on 2024-09-28 16:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_parent_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_created']},
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='IDX_comments_datecreated',
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-date_created'], name='IDX_comments_datecreated'),
        ),
    ]
