from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader

# Create your views here.
def page1(request):
    return render(request, 'page1.html')

def page2(request):
    return render(request, 'page2.html')

def qrcode(request):
    return render(request, 'qrcode.html')

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('page1/index.html')
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
