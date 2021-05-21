from django.urls import path
from .views import base_view, question_view, answer_view, comment_view

app_name = 'pybo'   # 네임스페이스 추가

urlpatterns = [
    # base_view
    path('', base_view.index, name = 'index'),  # /pybo/ -> index
    path('<int:question_id>/', base_view.detail, name = 'detail'), # /pybo/2 -> detail
    # question_view
    path('question/create/', question_view.question_create, name = 'question_create'),
    path('question/modify/<int:question_id>/', question_view.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', question_view.question_delete, name = 'question_delete'),
    # answer_view
    path('answer/create/<int:question_id>/', answer_view.answer_create, name = 'answer_create'),
    path('answer/modify/<int:answer_id>/', answer_view.answer_modify, name = 'answer_modify'),
    path('answer/delete/<int:answer_id>', answer_view.answer_delete, name = 'answer_delete'),
    # comment_view
    path('comment/create/question/<int:question_id>/', comment_view.comment_create_question, name = 'comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_view.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_view.comment_delete_question, name='comment_delete_question'),
    # comment_view
    path('comment/create/answer/<int:answer_id>/', comment_view.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_view.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_view.comment_delete_answer, name='comment_delete_answer'),

]
