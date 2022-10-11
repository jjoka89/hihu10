from django.urls import path

from . import views

urlpatterns = [
    path('home_Seosan/', views.seosan),
    path('home_Taean/', views.taean),
    path('', views.home),
    path('school_number/', views.SchoolNumberlist.as_view()),
    path('major/', views.major),
    path('major/majorA/', views.majorA),
    path('major/majorB/', views.majorB),
    path('major/majorC/', views.majorC),
    path('major/majorD/', views.majorD),
    path('major/majorE/', views.majorE),
    path('major/majorF/', views.majorF),
    path('major_number/', views.MajorNumberlist.as_view()),
    # /blog/category/slug(ex.문화예술)/ url연결 - 카테고리별 분류된 페이지
    path('category/<str:학부>/', views.faculty_page),
    path('faculty_number_list/', views.Facultylist.as_view()),
    path('bus/', views.bus, name='bus_tae'),
]
