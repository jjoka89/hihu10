from django.shortcuts import render, redirect, get_object_or_404

#from .models import Restaurant
from .models import Restaurant, Category

#def restaurant(request):
#    return render(request, 'restaurant.html')

"""def restaurant(request):
    restaurants = Restaurant.objects.filter().order_by('-pk')
    return render(request, 'restaurant.html', {'restaurants':restaurants})

def restaurantData(request): # 데이터를 저장하는 함수
    if request.method == 'POST' or request.method == 'FILES':
        restaurants = Restaurant()
        restaurants.name = request.POST['name']
        restaurants.title = request.POST['title']
        restaurants.logo = request.FILES['logo']
        restaurants.menu = request.FILES['menu']
        restaurants.call = request.POST['call']
        restaurants.save()
    return redirect('restaurant')

def detail(request, restaurant_id):
    restaurant_detail = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'detail.html', {'restaurant_detail':restaurant_detail})"""


"""def category(request, category_title):
    restaurants = Restaurant.objects.filter().order_by(category=category_title)
    categories = Category.objects.all()
    return render(request, 'category.html', {'category_title':category_title, 'restaurants':restaurants, 'categories':categories})"""

def category(request):
    categories = Category.objects.filter().order_by('-pk')
    return render(request, 'category.html', {'categories':categories})

def categoryData(request):
    if request.method == 'POST' or request.method == 'FILES':
        categories = Category()
        #categories.name = request.POST['name']
        categories.title = request.POST['title']
        categories.image = request.FILES['image']
        categories.save()
    return redirect('category')

def restaurant(request, category_id):
    restaurants = Restaurant.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    #restaurants = get_object_or_404(Restaurant.objects.filter(category_id=category_id)) # MultipleObjectsReturned at /restaurant/1 에러 발생
    return render(request, 'restaurant.html', {'category_id':category_id,'restaurants':restaurants, 'categories':categories})

def restaurantData(request): # 데이터를 저장하는 함수
    if request.method == 'POST' or request.method == 'FILES':
        restaurants = Restaurant()
        #restaurants.name = request.POST['name']
        restaurants.category = request.POST['category']
        restaurants.title = request.POST['title']
        restaurants.logo = request.FILES['logo']
        restaurants.menu1 = request.FILES['menu1']
        restaurants.menu2 = request.FILES['menu2']
        restaurants.menu3 = request.FILES['menu3']
        restaurants.call = request.POST['call']
        restaurants.open_close = request.POST['open_close']
        restaurants.close_day = request.POST['close_day']
        restaurants.save()
    return redirect('restaurant')

def detail(request, restaurant_id):
    restaurant_detail = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'detail.html', {'restaurant_detail':restaurant_detail})