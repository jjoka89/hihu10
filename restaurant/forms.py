from django import forms
#from .models import Restaurant
from .models import Restaurant, Category

"""class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'"""

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'