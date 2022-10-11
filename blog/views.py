from .forms import UserUpdateForm
from distutils.log import Log
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment, Dong
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.db.models import Q
from django.contrib.auth import authenticate, login
from blog.forms import UserForm
# /blog/페이지 클래스 생성 + ordering = 'pk'란 게시물의 순서를 최신순으로 바꿔주는 것


class PostList(ListView):
    model = Post
    ordering = '-pk'
    #paginate_by = 5

    # 카테고리 뷰 함수 생성(딕셔너리로 처리한다 - 첫번째 게시물의 카테고리는 ??이다 관계 형성)
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['카테고리'] = Category.objects.all()  # 카테고리가 있는 게시물 개수
        context['no_category_post_count'] = Post.objects.filter(
            카테고리=None).count()  # 카테고리가 없는 게시물 개수
        return context  # 카테고리 저장된 변수 리턴


def category_page(request, slug):  # 카테고리 별로 정렬된 페이지
    # 카테고리가 없으면(category_page함수의 slug인자로 'no_category'가 넘어오는 경우)
    if slug == 'no_category':
        카테고리 = '미분류'
        post_list = Post.objects.filter(카테고리=None)  # 카테고리가 미분류인 것들만 보여준다.
    else:
        # category_page함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 불러온다.
        카테고리 = Category.objects.get(slug=slug)
        # 동일한 카테고리인 게시물을 보여준다.

        post_list = Post.objects.filter(카테고리=카테고리).order_by('-pk')

    return render(  # render함수는 방문자에게 blog/post_list.html을 보내준다.(장고가 기본적으로 제공하는 함수)
        request,
        'blog/post_list.html',  # 템플릿은 post_list.html 사용
        {
            'post_list': post_list,
            '카테고리': Category.objects.all(),  # 모든 카테고리 레코드를 categories 저장
            # 미분류 카테고리 개수 알려줍니다.
            'no_category_post_count': Post.objects.filter(카테고리=None).count(),
            '게시물종류': 카테고리,  # 페이지 타이틀 옆에 카테고리 이름을 알려줍니다.
        }
    )

# 게시물 자세히 보기 누를 시 들어가는 페이지 뷰 클래스 생성


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):  # PostList클래스와 동일
        # 기본 구현을 호출해 context를 가져온다.
        context = super(PostDetail, self).get_context_data()
        # 모든 카테고리 레코드를 context[]에 저장
        context['카테고리'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(
            카테고리=None).count()  # 미분류 카테고리 개수 구하기
        # post_detail에서 comment_form사용 가능
        context['comment_form'] = CommentForm
        return context

# PostCreate이란 class 생성 후 model이라는 변수에 models.py파일에 있는 Post함수를 대입


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post  # Post모델 사용
    fields = ['제목', '내용',  '카테고리']  # Post 모델에 사용할 제목, 요약문, 내용 등

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.작성자 = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UpdateView):  # 게시물 수정하는 기능 추가
    model = Post
    fields = ['제목', '내용', '카테고리']  # Post 모델에 사용할 제목, 요약문, 내용 등

    template_name = 'blog/post_update_form.html'  # 템플릿 파일은 post_update_form.html로 설정

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().작성자:  # 로그인한 유저가 게시물 작성자와 같으면
            # 게시물 수정 가능
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # 그렇지 않으면 오류


def new_comment(request, pk):  # 댓글 기능 추가
    if request.user.is_authenticated:  # 로그인하지 않은 상태에서 댓글 폼이 포스트 상세 페이지에 보이지 않게 설정
        # 댓글 달 포스트의 pk값을 가져온다.(해당 pk가 없을 경우 오류를 발생시킨다.)
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':  # 댓글 전달 방식이 POST방식이면
            comment_form = CommentForm(request.POST)  # 댓글 내용 저장
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.게시물 = post
                comment.작성자 = request.user
                comment.save()
                # comment의 url로 리다이렉트(해당 포스트의 댓글 위치로 이동)
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:  # 비정상적인 방법으로 new_comment에 접근 시도를 막아주는 기능
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().작성자:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.게시물
    if request.user.is_authenticated and request.user == comment.작성자:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated and request.user == post.작성자:
        post.delete()
        return redirect('/blog')
    else:
        raise PermissionDenied


class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(제목__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context


class Dongari(ListView):
    model = Dong
    ordering = '-pk'
    #paginate_by = 5
    fields = ['동아리명', '동아리내용', '요약문', '동아리로고',
              '활동사진']  # Post 모델에 사용할 제목, 요약문, 내용 등등

    #template_name = 'blog/dongari.html'

    # 카테고리 뷰 함수 생성(딕셔너리로 처리한다 - 첫번째 게시물의 카테고리는 ??이다 관계 형성)
    def get_context_data(self, **kwargs):
        context = super(Dongari, self).get_context_data()

        return context


class DongSearch(Dongari):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        dong_list = Dong.objects.filter(
            Q(동아리명__contains=q)
        ).distinct()
        return dong_list

    def get_context_data(self, **kwargs):
        context = super(DongSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context


class DongDetail(DetailView):
    model = Dong

    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, **kwargs):  # PostList클래스와 동일
        # 기본 구현을 호출해 context를 가져온다.
        context = super(DongDetail, self).get_context_data()
        return context

# 회원가입3


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,
                                password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/blog/')
    else:
        form = UserForm()
    return render(request, 'blog/signup.html', {'form': form})


def update(request):
    if request.method == "POST":
        # 이게 없으면 수정할 때마다 새로운 계정을 만든다.
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # 폼값을 불러오고 저장
            return redirect('/blog/')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/user_update.html', {'form': form})


def myPost(request):
    user = request.user
    posts = Post.objects.filter(작성자=user).order_by('-pk')
    likes = Post.objects.filter(
        Q(like_users=request.user)
    )

    if user.is_authenticated is False:
        return redirect("login")

    return render(request, 'blog/myPost.html', {'user': user, 'likes': likes, 'posts': posts, })


def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # success_url = post.get_absolute_url()
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)

    else:
        post.like_users.add(request.user)
    return redirect(post.get_absolute_url())


def bus(request):
    return render(request, 'blog/bus.html')
