from django.apps import AppConfig

#blog라는 앱 생성
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'