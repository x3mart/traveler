# Generated by Django 3.2.7 on 2021-10-14 11:06

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_auto_20211011_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourbasic',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание тура'),
        ),
        migrations.AddField(
            model_name='tourbasic',
            name='plan',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Чем займемся'),
        ),
        migrations.AlterField(
            model_name='tourday',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Описание'),
        ),
    ]