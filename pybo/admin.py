from django.contrib import admin
from .models import Answer, Question
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] # 제목으로 질문 검색

class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['question']

# admin 에서 모델 관리하기
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)