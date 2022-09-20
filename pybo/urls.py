from . import views
from django.urls import path, include

app_name = 'pybo'
urlpatterns = [
    # path('', views.index),
    # path('<int:question_id>', views.detail),
    path('', views.IndexView.as_view(), name = 'index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('answer/create/<int:pk>', views.answer_create, name='answer_create'),
    path('question_create', views.question_create, name='question_create'),
]
