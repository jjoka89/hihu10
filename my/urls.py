from django.urls import path, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('', include('single_pages.urls')),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
