from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from blog.forms import MyPasswordChangeForm

urlpatterns = [
    # 게시물 수정하는 페이지 url연결
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    # /blog/category/slug(ex.문화예술)/ url연결 - 카테고리별 분류된 페이지
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    # /blog/숫자/ url연결 - 게시물 디테일 페이지(첫번째 게시물 페이지의 숫자는 1)
    path('<int:pk>/', views.PostDetail.as_view()),
    # /blog/ url연결 - 게시물 목록 페이지
    path('', views.PostList.as_view(), name='blog'),
    # /blog/create_post/ url연결 - 게시물 작성 페이지
    path('create_post/', views.PostCreate.as_view()),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('delete_post/<int:pk>/', views.delete_post),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('dongari/', views.Dongari.as_view()),
    path('search_dong/<str:q>/', views.DongSearch.as_view()),
    # /blog/숫자/ url연결 - 게시물 디테일 페이지(첫번째 게시물 페이지의 숫자는 1)
    path('dongari/<int:pk>/', views.DongDetail.as_view()),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='blog/logout.html'), name="password_reset_complete"),
    path('update_info/', views.update, name='update'),

    path('change_password/',
         PasswordChangeView.as_view(
             template_name='blog/change_password.html',
             success_url=reverse_lazy('blog'),
             form_class=MyPasswordChangeForm
         ),
         name="password_change"),
    path('mypost/', views.myPost, name='mypost'),
    path('<int:pk>/like/', views.like_post, name="like_post"),
    path('bus/', views.bus, name='bus'),
]
