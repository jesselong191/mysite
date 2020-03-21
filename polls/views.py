from django.shortcuts import render,get_object_or_404
from django.http import  HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
#导入Django通用视图
from django.views import generic
'''
视图
'''

class IndexView(generic.ListView):
    template_name =  'polls/index.html'
    context_object_name = 'lastest_question_list'

    def get_queryset(self):
        """Return the lastfive publised questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    """指定模型名"""
    model = Question
    """指定模板名"""
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':'You didnot select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))