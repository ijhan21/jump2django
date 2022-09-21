from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Answer
from django.views import generic
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    page = request.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date') # 앞에 - 때문에 역순 정렬
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    # context = {'question_list':question_list}
    context = {'question_list':page_obj}
    # return HttpResponse("hello")
    return render(request, 'pybo/question_list.html', context)

def detail(request, pk):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=pk)
    context = {'question':question}
    return render(request, 'pybo/question_detail.html', context)
"""
class IndexView(generic.ListView):
    def get_queryset(self):
        return Question.objects.order_by('-create_date')

class DetailView(generic.DetailView):
    model = Question
"""
@login_required
def answer_create(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", pk=pk)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}    
    return render(request, 'pybo/question_detail.html', context)

@login_required
def question_create(request):
    if request.method =="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # commit=False : 임시저장. 그냥 저장하면 create_date가 없어서 오류
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    form = QuestionForm()
    return render(request, 'pybo/question_form.html',{'form':form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user !=question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', pk=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', pk=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user !=answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', answer_id=answer.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', pk=answer.question.id)
    else:
        form = QuestionForm(instance=answer)
    context = {'answer':answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', pk=answer.question.id)
    answer.delete()
    return redirect('pybo:detail',pk=answer.question.id)