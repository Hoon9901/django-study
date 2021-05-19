from django.urls import path
from . import views

app_name = 'pybo'   # 네임스페이스 추가

urlpatterns = [
    # 질문
    path('', views.index, name = 'index'),  # /pybo/ -> index
    path('<int:question_id>/', views.detail, name = 'detail'), # /pybo/2 -> detail
    path('question/create/', views.question_create, name = 'question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name = 'question_delete'),
    # 답변
    path('answer/create/<int:question_id>/', views.answer_create, name = 'answer_create'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name = 'answer_modify'),
    path('answer/delete/<int:answer_id>', views.answer_delete, name = 'answer_delete'),
]
