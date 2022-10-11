from django.contrib import admin

#from .models import Restaurant

#admin.site.register(Restaurant)

from .models import Category, Restaurant

#class CategoryAdmin(admin.ModelAdmin):
#    search_fields = ['title']

admin.site.register(Category)
admin.site.register(Restaurant)
