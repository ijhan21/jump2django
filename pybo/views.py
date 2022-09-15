from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.
def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    question_list = Question.objects.order_by('-create_date') # 앞에 - 때문에 역순 정렬
    context = {'question_list':question_list}
    # return HttpResponse("hello")
    return render(request, 'pybo/question_list.html', context)