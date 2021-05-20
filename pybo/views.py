from django.core import paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Question, Answer, Comment
from .forms import AnswerForm, QuestionForm, CommentForm
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

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """ 질문 수정 """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')  # 넌 필드 오류
        return redirect('pybo:detail', question_id = question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)    # question을 기본값으로, form의 입력값들을 덮어써사 Form 생성
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date  = timezone.now() # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)  # 기존 저장된 질문 반영된 상태에서 수정
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """ 질문 삭제 """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author :
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()   # js 함수 호출
    return redirect('pybo:index')

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
def answer_modify(request, answer_id):
    # 답변 수정
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now() # 수정 시각
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)
    else :
        form = AnswerForm(instance=answer)
    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    # 답변 삭제
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else :
        answer.delete() # js 함수 호출
    return redirect('pybo:detail', question_id = answer.question.id)

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """ 댓글 등록 """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST" :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question # 짓문에 댓글 달리므로, question 저장
            comment.save()
            return redirect('pybo:detail', question_id = question_id)
    else :
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """ 질문댓글수정  """
    print("heeloo")
    comment = get_object_or_404(Comment, pk=comment_id) 
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)    # 기존 댓글을 폼에 반영하여 지속적인 수정
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """ 질문댓글삭제 """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()    # 삭제 js 함수 호출
    return redirect('pybo:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """ 답글댓글등록 """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id) # 질문 참조
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """ 답글댓글수정 """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context) # 기존 폼 이용


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """ 답글댓글삭제 """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)
