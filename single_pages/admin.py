from django.contrib import admin
from .models import School, Major, Faculty

# Register your models here.
admin.site.register(School)
admin.site.register(Major) 

admin.site.register(Faculty)  #카테고리 작성 관리자 페이지 추가