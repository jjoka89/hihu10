from django.db import models
# User모델을 사용해야 하므로(장고에서 기본으로 제공하는 모델)
from django.contrib.auth.models import User
import os
from datetime import datetime, timedelta, timezone
from django.conf import settings
# Create your models here.


class Category(models.Model):  # 카테고리 모델 생성
    # unique=True 코드를 넣으면 동일한 name을 갖는 카테고리를 만들 수 없다(길이 제한이 있는 문자열)
    게시물종류 = models.CharField(max_length=50, unique=True)
    # allow_unique=True 코드를 넣으면 SlugField 한글로 지원(길이 제한이 없는 문자열)
    slug = models.SlugField(max_length=200, allow_unicode=True)

    def __str__(self):
        return self.게시물종류  # 카테고리 이름 리턴

    def get_absolute_url(self):
        # 카테코리 관리 페이지에서 view on site 버튼 생성 후 버튼 누르면 해당 카테고리 페이지로 이동
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = '카테고리'  # 관리자 페이지에서 카테고리 목록 이름을 categorys에서 categories로 변경

# views.py파일에서 사용하기 위한 게시물 class생성


class Post(models.Model):
    제목 = models.CharField(max_length=30)  # title은 문자열로 최대 길이 30(게시물 제목)
    내용 = models.TextField()  # content는 텍스트형(게시물 내용)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_posts", blank=True)
    # 대표사진 이미지를 저장할 폴더의 경로 규칙 지정(blank=True는 필드를 채우지 않더라도 경고 표시가 안뜨게 + blog라는 폴더 아래 images라는 폴더를 만들고 연도, 월, 일 폴더까지 내려간 위치에 저장하도록 설정)
    대표사진 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 파일사진 이미지를 저장할 폴더의 경로 규칙 지정(blank=True는 필드를 채우지 않더라도 경고 표시가 안뜨게 + blog라는 폴더 아래 files라는 폴더를 만들고 연도, 월, 일 폴더까지 내려간 위치에 저장하도록 설정)
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)

    # 게시물 생성 시간을 자동으로 현재 시간으로 설정(최초 저장시에만 저장)
    작성일 = models.DateTimeField(auto_now_add=True)
    # 게시물 업데이트 시간을 현재 시간으로 설정(업데이트 될 때마다 저장)
    updated_at = models.DateTimeField(auto_now=True)

    # 포스트의 작성자가 데이터베이스에서 삭제되었을 때 작성자명을 빈칸으로 둔다(User객체 사용을 위해서 ForeignKey사용 - 상속)
    작성자 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # 카테고리가 삭제되었을 때 카테고리명을 빈칸으로 둔다.
    카테고리 = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):  # [제목번호]제목 :: 작성자명 <-- 이와 같은 형식으로 나올 수 있도록 설정(관리자 페이지)
        return f'[{self.pk}]{self.제목} :: {self.작성자}'
    # pk는 각 레코드의 고유값(1,2....)
    # self.title로 제목 나타내기

    def get_absolute_url(self):  # 게시물 관리 페이지에서 view on site 버튼 생성 후 버튼 누르면 해당 게시물 페이지로 이동
        return f'/blog/{self.pk}/'

    def get_file_name(self):  # 다운로드 버튼에 파일명 보이도록 설정
        return os.path.basename(self.file_upload.name)

    def get_file_exit(self):  # 파일명 저장 공간
        return self.get_file_name().split('.')[-1]

    class Meta:
        verbose_name_plural = '게시물'  # 관리자 페이지에서 카테고리 목록 이름을 categorys에서 categories로 변경


class Comment(models.Model):  # 댓글 모델 클래스 추가
    # 어떤 게시물의 대한 댓글인지를 저장할 post필드
    # 게시물 삭제시 해당 게시물의 댓글도 삭제
    게시물 = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 작성자를 저장할 author필드
    # 포스트의 작성자가 데이터베이스에서 삭제되었을 때 작성자명을 빈칸으로 둔다(User객체 사용을 위해서 ForeignKey사용 - 상속)
    작성자 = models.ForeignKey(User, on_delete=models.CASCADE)
    # 내용을 저장할 content필드

    내용 = models.TextField()
    # 작성일시와 수정일시를 담을 created_at, modified필드
    작성일 = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # 댓글 작성자명과 내용 보여주도록 설정
    def __str__(self):
        return f'{self.작성자}::{self.내용}'

    # 관리자 서버에서 view on site 버튼 생성하고 버튼 누를 시 페이지 맨 위를 보여주는게 아닌 해당 댓글 위치로 바로 보여주도록 설정
    def get_absolute_url(self):
        return f'{self.게시물.get_absolute_url()}#comment-{self.pk}'

    class Meta:
        verbose_name_plural = '댓글'  # 관리자 페이지에서 카테고리 목록 이름을 categorys에서 categories로 변경


class Dong(models.Model):  # 댓글 모델 클래스 추가
    # 어떤 게시물의 대한 댓글인지를 저장할 post필드
    동아리명 = models.CharField(max_length=30)  # title은 문자열로 최대 길이 30(게시물 제목)
    # 작성자를 저장할 author필드
    # 내용을 저장할 content필드
    동아리내용 = models.TextField()
    요약문 = models.CharField(max_length=100, blank=True)
    # 포스트의 작성자가 데이터베이스에서 삭제되었을 때 작성자명을 빈칸으로 둔다(User객체 사용을 위해서 ForeignKey사용 - 상속)
    작성자 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    동아리로고 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 대표사진 이미지를 저장할 폴더의 경로 규칙 지정(blank=True는 필드를 채우지 않더라도 경고 표시가 안뜨게 + blog라는 폴더 아래 images라는 폴더를 만들고 연도, 월, 일 폴더까지 내려간 위치에 저장하도록 설정)
    활동사진 = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    # 파일사진 이미지를 저장할 폴더의 경로 규칙 지정(blank=True는 필드를 채우지 않더라도 경고 표시가 안뜨게 + blog라는 폴더 아래 files라는 폴더를 만들고 연도, 월, 일 폴더까지 내려간 위치에 저장하도록 설정)

    def __str__(self):  # [제목번호]제목 :: 작성자명 <-- 이와 같은 형식으로 나올 수 있도록 설정(관리자 페이지)
        return f'{self.동아리명}'
    # pk는 각 레코드의 고유값(1,2....)
    # self.title로 제목 나타내기

    def get_absolute_url(self):  # 게시물 관리 페이지에서 view on site 버튼 생성 후 버튼 누르면 해당 게시물 페이지로 이동
        return f'/blog/dongari/{self.pk}/'

    class Meta:
        verbose_name_plural = '동아리'  # 관리자 페이지에서 카테고리 목록 이름을 categorys에서 categories로 변경


class Category_res(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='media/image/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        verbose_name_plural = '식당종류'

    def __str__(self):
        return self.title


class Restaurant(models.Model):
    category = models.ForeignKey(
        Category, related_name='restaurant_featured', on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE) # 이것도 가능
    식당이름 = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='media/logo/%Y/%m/%d/', blank=True, null=True)
    메뉴 = models.ImageField(
        upload_to='media/menu/%Y/%m/%d/', blank=True, null=True)
    전화번호 = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = '식당'

    def __str__(self):
        return self.식당이름
