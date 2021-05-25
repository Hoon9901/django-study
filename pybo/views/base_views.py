from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.db.models import Q

def index(request):
    """ 목록 출력 """
    # 입력 파라미터, localhost:8000/pybo/?page=1
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '')      # 검색어
    # 조회
    question_list = Question.objects.order_by('-create_date')   # 작성일시의 역순 정렬
    if kw : # 검색어 존재할시
        question_list = question_list.filter(   # 필드 접근은 __ 사용, icontains -> 대소문자 구별안함
            Q(subject__icontains = kw) |        # 제목 
            Q(content__icontains = kw) |        # 내용
            Q(author__username__icontains = kw) |   # 글쓴이
            Q(answer__author__username__icontains = kw)   # 답변 글쓴이
        ).distinct()    # 중복 제거 # Q(answer_content_icontain) <- 답변 내용
    # 페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 10개 씩
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages

    context = {'question_list' : page_obj, 'page' : page, 'kw' : kw, 'last_page' : last_page}
    return render(request, 'pybo/question_list.html', context)  # 템플릿

def detail(request, question_id):
    # 내용 출력
    # 존재하지 않는 페이지 접속시 404 출력, 기본키를 이용해 객체 반환
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)
