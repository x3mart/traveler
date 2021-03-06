# Generated by Django 3.2.7 on 2022-05-21 18:46

import articles.models
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=articles.models.article_path, verbose_name='Главное фото')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('reading_time', models.PositiveIntegerField(blank=True, null=True, verbose_name='Время чтения')),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=articles.models.article_path, verbose_name='Главное фото')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Текст')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата публикации')),
                ('reading_time', models.PositiveIntegerField(blank=True, null=True, verbose_name='Время чтения')),
                ('is_active', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
