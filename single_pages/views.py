from django.shortcuts import render
from .models import School, Major, Faculty
from django.views.generic import ListView
import re

# Create your views here.


def home(request):
    return render(
        request,
        template_name='single_pages/hihuHome.html'
    )


def seosan(request):
    return render(
        request,
        template_name='single_pages/home_Seosan.html'
    )


def taean(request):
    return render(
        request,
        template_name='single_pages/home_Taean.html'
    )


def major(request):
    return render(
        request,
        template_name='single_pages/hihuMajor.html'
    )


def majorA(request):
    return render(
        request,
        'single_pages/hihuMajorA.html'
    )


def majorB(request):
    return render(
        request,
        'single_pages/hihuMajorB.html'
    )


def majorC(request):
    return render(
        request,
        'single_pages/hihuMajorC.html'
    )


def majorD(request):
    return render(
        request,
        'single_pages/hihuMajorD.html'
    )


def majorE(request):
    return render(
        request,
        'single_pages/hihuMajorE.html'
    )


def majorF(request):
    return render(
        request,
        'single_pages/hihuMajorF.html'
    )


class SchoolNumberlist(ListView):
    model = School
    fields = ['부서', '전화번호']  # Post 모델에 사용할 제목, 요약문, 내용 등등

    template_name = 'single_pages/school_number.html'

    # 카테고리 뷰 함수 생성(딕셔너리로 처리한다 - 첫번째 게시물의 카테고리는 ??이다 관계 형성)
    def get_context_data(self, **kwargs):
        context = super(SchoolNumberlist, self).get_context_data()

        return context


class Facultylist(ListView):
    model = Faculty
    fields = ['학부']

    template_name = 'single_pages/faculty.html'

    def get_context_data(self, **kwargs):
        context = super(Facultylist, self).get_context_data()

        return context


def faculty_page(request, 학부):  # 카테고리 별로 정렬된 페이지
    # category_page함수의 인자로 받은 slug와 동일한 slug를 갖는 카테고리를 불러온다.
    학부 = Faculty.objects.get(학부=학부)
    # 동일한 카테고리인 게시물을 보여준다.
    major_list = Major.objects.filter(학부=학부)

    return render(  # render함수는 방문자에게 blog/post_list.html을 보내준다.(장고가 기본적으로 제공하는 함수)
        request,
        'single_pages/major_number.html',  # 템플릿은 post_list.html 사용
        {
            'major_list': major_list,
            '학부': Faculty.objects.all(),  # 모든 카테고리 레코드를 categories 저장
            # 미분류 카테고리 개수 알려줍니다.
            '학부': 학부,  # 페이지 타이틀 옆에 카테고리 이름을 알려줍니다.
        }
    )


class MajorNumberlist(ListView):
    model = Major
    fields = ['학과', '전화번호', '학부']  # Post 모델에 사용할 제목, 요약문, 내용 등등

    template_name = 'single_pages/major_number.html'

    # 카테고리 뷰 함수 생성(딕셔너리로 처리한다 - 첫번째 게시물의 카테고리는 ??이다 관계 형성)
    def get_context_data(self, **kwargs):
        context = super(MajorNumberlist, self).get_context_data()
        context['학부'] = Faculty.objects.all()  # 카테고리가 있는 게시물 개수
        return context  # 카테고리 저장된 변수 리턴


def bus(request):
    return render(request, 'single_pages/bus_tae.html')
