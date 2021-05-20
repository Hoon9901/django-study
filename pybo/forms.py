from django import forms
from django.forms import fields, widgets
from .models import Question, Answer, Comment

# 모델 폼(모델과 연결 된 폼)
class QuestionForm(forms.ModelForm):

    # 모델 폼이 사용할 모델, 필드
    class Meta :
        model = Question
        fields = ['subject', 'content']
        # 한글 표시
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }

class AnswerForm(forms.ModelForm) :
    class Meta :
        model = Answer
        fields = ['content']
        lables ={
            'content' : '답변내용',
        }

#댓글 폼
class CommentForm(forms.ModelForm):
    class Meta: # 모델, 필드
        model = Comment
        fields = ['content']
        labels = {  # 한글
            'content' : '댓글내용',
        }
        