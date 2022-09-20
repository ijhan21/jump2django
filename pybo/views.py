from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.views import generic
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
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

def answer_create(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", pk=pk)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}    
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):
    if request.method =="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # commit=False : 임시저장. 그냥 저장하면 create_date가 없어서 오류
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    form = QuestionForm()
    return render(request, 'pybo/question_form.html',{'form':form})

