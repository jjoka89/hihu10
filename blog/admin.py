from django.contrib import admin
from .models import Post, Category, Comment, Dong

# 관리자 사이트 생성
admin.site.register(Post)  #게시물 작성 관리자 페이지 추가
admin.site.register(Comment)  #댓글 작성 관리자 페이지 추가
admin.site.register(Dong)

class CategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug' : ('게시물종류', )}     #카테고리 추가할 시 자동으로 slug칸에 카테고리 넣기(url에 적절하지 않은 문자 있을 시 적절한 것으로 변경)
    
admin.site.register(Category, CategoryAdmin)  #카테고리 작성 관리자 페이지 추가