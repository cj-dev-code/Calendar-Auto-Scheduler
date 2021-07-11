from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from calendarauto.models import Article

# If the url is going to use varibles, then they must be listed here
# in the function name if it is a custom view i.e. what we have here
def calendarView(request, year, month, week):
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
    
    
    
class todoView(generic.ListView):
    template_name = 'calendarauto/todolist.html'
    
    
    
#def mysteryView():
    