from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

<<<<<<< HEAD
import datetime


#from calendarauto.models import Article

# If the url is going to use varibles, then they must be listed here
# in the function name if it is a custom view i.e. what we have here
def CalendarView(request, year, month, day):
=======
# If the url is going to use varibles, then they must be listed here
# in the function name if it is a custom view i.e. what we have here
def CalendarView(request, year, month, week):
>>>>>>> 83fb07511f767675616159fd872ed54bc1d62e6e
    #template_name = 'calendarauto/calendar.html'
    #queryset = Article.objects.all()
    #date_field = "pub_date"
    #week_format = "%W"
    #allow_future = True
    #try:
    #    article = Article.objects.get(pk=question_id)
    #except Article.DoesNotExist:
    #    raise Http404("Article does not exist")
    #if (datetime.datetime(year = year, month, day)):
    isValidDate = True
    try:
        datetime.datetime(year, month, day)
    except:
        isValidDate = False
            
    if (isValidDate):
        today = datetime.datetime(year, month, day)
    else:
        today = datetime.datetime.now()
        
    #else:
    #    today = datetime.now()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = today + datetime.timedelta(6 - idx)
    return render(request, 'calendarauto/calendar.html', {'sunday' : sun, 'saturday' : sat, 'day' : day})
    
    
    
class TodoView(generic.ListView):
    template_name = 'calendarauto/todolist.html'
    
    
def MysteryView(request):
    #template_name = 'calendarauto/calendar.html'
    #queryset = Article.objects.all()
    #date_field = "pub_date"
    #week_format = "%W"
    #allow_future = True
    #try:
    #    article = Article.objects.get(pk=question_id)
    #except Article.DoesNotExist:
    #    raise Http404("Article does not exist")
    return render(request, 'calendarauto/calendar.html')
    
    
#def mysteryView():
    