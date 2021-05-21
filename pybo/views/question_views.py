from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

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
            return redirect('pybo:detail', question_id = question.id)   # 질문 화면으로 이동
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
