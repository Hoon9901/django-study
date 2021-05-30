from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer
from django.db.models import Q, Count

def index(request):
    """ 목록 출력 """
    # 입력 파라미터, localhost:8000/pybo/?page=1
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '')      # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준 -> 최근순
    # 정렬 annotate 함수 -> 모델 기존필드에 함수 파라미터로 해당하는 필드를 임시 추가
    if so == 'recommend':   # 추천 순
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':   # 답변 순
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    elif so == 'view':      # 조회 순
        question_list = Question.objects.order_by('-view', '-create_date')
    else:   #  # 작성일자, order_by에 두개 이상의 인자일씨 1번째 항목부터 우선순위, 추천수같으면 최신순으로 정렬됨
        question_list = Question.objects.order_by('-create_date')  
    
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

    context = {'question_list' : page_obj, 'page' : page, 'kw' : kw, 'so' : so,'last_page' : last_page}
    return render(request, 'pybo/question_list.html', context)  # 템플릿

def detail(request, question_id):
    # 내용 출력
    # 존재하지 않는 페이지 접속시 404 출력, 기본키를 이용해 객체 반환
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        answer_list = Answer.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = Answer.objects.annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:  # recent
        answer_list = Answer.objects.order_by('-create_date')

    question = get_object_or_404(Question, pk=question_id)

    paginator = Paginator(answer_list, 10)
    page_obj = paginator.get_page(page)
    last_page = paginator.num_pages
    answer_count = page_obj.count
    context = {'answer_list' : page_obj, 'question' : question, 'page' : page
                ,'so' : so, 'answer_count' : answer_count, 'last_page' : last_page}
    return render(request, 'pybo/question_detail.html', context)
