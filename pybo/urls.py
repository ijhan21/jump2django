from . import views
from django.urls import path, include


urlpatterns = [
    # path('', views.index),
    # path('<int:question_id>', views.detail),
    path('', views.IndexView.as_view()),
    path('<int:pk>/', views.DetailView.as_view())
]
