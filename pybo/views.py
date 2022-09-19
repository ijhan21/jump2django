from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question
from django.views import generic
# Create your views here.
def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    question_list = Question.objects.order_by('-create_date') # 앞에 - 때문에 역순 정렬
    context = {'question_list':question_list}
    # return HttpResponse("hello")
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)

class IndexView(generic.ListView):
    def get_queryset(self):
        return Question.objects.order_by('-create_date')

class DetailView(generic.DetailView):
    model = Question