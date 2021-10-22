# Generated by Django 3.2.7 on 2021-10-22 10:44

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_customer'),
        ('tours', '0015_tourbasic_wallpaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Отзыв')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_tours_reviews', to='accounts.customer', verbose_name='Тур')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_reviews', to='tours.tourbasic', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Отзыв о туре',
                'verbose_name_plural': 'Отзывы о турах',
            },
        ),
        migrations.CreateModel(
            name='ExpertReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', ckeditor.fields.RichTextField(verbose_name='Отзыв')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_experts_reviews', to='accounts.customer', verbose_name='Тур')),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expert_reviews', to='accounts.expert', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Отзыв об эксперте',
                'verbose_name_plural': 'Отзывы об экспертах',
            },
        ),
    ]
