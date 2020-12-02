# Generated by Django 2.2.17 on 2020-11-27 16:03

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_newsletters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='When adding images, please ensure to set the width no larger than 600px.', verbose_name='Email body'),
        ),
    ]