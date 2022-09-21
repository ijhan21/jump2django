from . import views
from django.urls import path, include

app_name = 'pybo'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.detail, name='detail'),
    # path('', views.IndexView.as_view(), name = 'index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('answer/create/<int:pk>', views.answer_create, name='answer_create'),
    path('question_create', views.question_create, name='question_create'),
    path('question_modify/<int:question_id>', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer_modify/<int:answer_id>', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
]
