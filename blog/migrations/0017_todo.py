# Generated by Django 4.0.3 on 2022-08-11 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_comment_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
    ]
