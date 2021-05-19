from django.db import models
from django.contrib.auth.models import User # username, password

# Create your models here.
# 질문 모델
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # ondelete -> 계정 삭제 시 다 삭제
    subject = models.CharField(max_length=200)  # 질문 제목
    content = models.TextField()                # 질문 내용
    create_date = models.DateTimeField()        # 작성 일시
    modify_date = models.DateTimeField(null = True, blank=True) # 수정 일시, null,blan -> 어떤 조건으로든 값을 비울숟있다

    def __str__(self):
        return self.subject
    #makemigrations, migrate 명령은 모델의 속성이 추가되거나 변경된 경우에 실행해야 하는 명령이다. 지금은 메서드가 추가된 것이므로 이 과정은 하지 않아도 된다.


# 답변 모델, 어떤 질문에 대한 답변이므로 Question 모델을 속성으로 가짐
class Answer(models.Model):
    # ForeignKey -> 다른 모델과의 연결
    # on_delete = models.CASCADE 답변에 연결된 질문 삭제시 답변도 함께 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    # 질문
    content = models.TextField()                # 답변 내용
    create_date = models.DateTimeField()        # 작성 일시
    modify_date = models.DateTimeField(null=True, blank=True)   # 수정 일시
