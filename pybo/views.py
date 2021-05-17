from django.core import paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Question, Answer
from .forms import AnswerForm, QuestionForm
from django.contrib.auth.decorators import login_required

# Create your views here.
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

@login_required(login_url='common:login')
def answer_create(request, question_id) :
    # 답변 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid() :
            answer = form.save(commit=False)
            answer.author = request.user # 로그인한 계정(user)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question_id)
    else :
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request) : 
    # 질문 등록
    if request.method == 'POST':    # 질문 저장
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 폼이 작성되있으면 작성된걸로 DB 저장
            question = form.save(commit=False)  # commit ->False (임시저장) why -> creaet_date 작성안되어있어서 오류 발생
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')   # 질문 화면으로 이동
    else : # GET 방식으로 질문등록화면 요청 (질문  등록)
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)