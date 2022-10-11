from django.db import models

from django.contrib.auth.models import User

"""class Restaurant(models.Model):
    name = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/logo/%Y/%m/%d/', blank=True, null=True)
    menu = models.ImageField(upload_to='media/menu/%Y/%m/%d/', blank=True, null=True)
    call = models.CharField(max_length=200)

    def __str__(self):
        return self.title"""

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/image/%Y/%m/%d/', blank=True, null=True)

    class Meta :
        verbose_name_plural='식당종류'

    def __str__(self):
        return self.title

class Restaurant(models.Model):
    category = models.ForeignKey(Category, related_name='restaurant_featured', on_delete=models.CASCADE)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE) # 이것도 가능
    title = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/logo/%Y/%m/%d/', blank=True, null=True)
    menu1 = models.FileField(upload_to='media/menu/%Y/%m/%d/', blank=True, null=True)
    menu2 = models.FileField(upload_to='media/menu/%Y/%m/%d/', blank=True, null=True)
    menu3 = models.FileField(upload_to='media/menu/%Y/%m/%d/', blank=True, null=True)
    
    call = models.CharField(max_length=200)
    open_close = models.TextField(max_length=200)
    close_day = models.CharField(max_length=200, blank=True)

    class Meta :
        verbose_name_plural='식당'

    def __str__(self):
        return self.title
    