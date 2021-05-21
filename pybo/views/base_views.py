import django
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer

def index(request):
    """ 목록 출력 """
    # 입력 파라미터, localhost:8000/pybo/?page=1
    page = request.GET.get('page', '1') # 페이지
    # 조회
    question_list = Question.objects.order_by('-create_date')   # 작성일시의 역순 정렬
    # 페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 10개 씩
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    context = {'question_list' : page_obj, 'last_page' : last_page}
    return render(request, 'pybo/question_list.html', context)  # 템플릿

def detail(request, question_id):
    # 내용 출력
    # 존재하지 않는 페이지 접속시 404 출력, 기본키를 이용해 객체 반환
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)
