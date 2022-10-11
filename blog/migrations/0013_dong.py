# Generated by Django 4.0.3 on 2022-08-07 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_rename_modiified_at_comment_modified_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('head_image', models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d/')),
                ('file_upload', models.FileField(blank=True, upload_to='blog/files/%Y/%m/%d/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]