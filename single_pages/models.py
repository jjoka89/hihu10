import datetime

from django.db import models

# Create your models here.
class School(models.Model) :
    부서=models.CharField(max_length=30)
    전화번호=models.TextField()
    
    def __str__(self):
        return f'[{self.pk}]{self.부서}'
    #pk는 각 레코드의 고유값(1,2....)
    #self.title로 제목 나타내기
    
    def get_absolute_url(self):
        return f''
    
    class Meta :
        verbose_name_plural='학교연락처'
    
class Faculty(models.Model) :      #카테고리 모델 생성
    학부=models.CharField(max_length=50, unique=True)      #unique=True 코드를 넣으면 동일한 name을 갖는 카테고리를 만들 수 없다(길이 제한이 있는 문자열)
    
    def __str__(self) :
        return self.학부        #카테고리 이름 리턴
    
    def get_absolute_url(self): 
        return f'/category/{self.학부}/'      #카테코리 관리 페이지에서 view on site 버튼 생성 후 버튼 누르면 해당 카테고리 페이지로 이동
    
    class Meta :
        verbose_name_plural='학부'       #관리자 페이지에서 카테고리 목록 이름을 categorys에서 categories로 변경
    
class Major(models.Model) :
    학과=models.CharField(max_length=30)
    전화번호=models.TextField()
    
    학부=models.ForeignKey(Faculty, null=True, blank=True, on_delete=models.SET_NULL)     #카테고리가 삭제되었을 때 카테고리명을 빈칸으로 둔다.

    def __str__(self):
        return f'[{self.pk}]{self.학과} - {self.학부}'
    #pk는 각 레코드의 고유값(1,2....)
    #self.title로 제목 나타내기
    
    def get_absolute_url(self):
        return f''
    
    class Meta :
        verbose_name_plural='학과' 
