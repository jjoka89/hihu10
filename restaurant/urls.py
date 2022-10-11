from django.urls import path
from . import views

urlpatterns = [
    #path('restaurant', views.restaurant, name='restaurant'),
    #path('detail/<int:restaurant_id>', views.detail, name='detail'),

    path('', views.category, name='category'),
    path('restaurant/<int:category_id>', views.restaurant, name='restaurant'),
    path('detail/<int:restaurant_id>', views.detail, name='detail'),
]

