from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime, time
import datetime

from .models import GenericTask, GenericHourBlock


#from calendarauto.models import Article

# If the url is going to use varibles, then they must be listed here
# in the function name if it is a custom view i.e. what we have here
def CalendarView(request, year, month, day):
    isValidDate = True
    try:
        datetime(year, month, day)
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
    context_object_name = 'task_list'
    
def MysteryView(request):
    return render(request, 'calendarauto/calendar.html')
    
def create_generic_task(deadline, hours_to_complete,
                    completed=False,scheduled=False, time_created=None, location='Default',
                    task_name='Default', task_description='Default',
                    do_after = None):
    est_time = time(int(hours_to_complete), int((hours_to_complete % 1)*60), 0)
    time_assigned = timezone.now() if time_created == None else time_created
    do_after = timezone.now() if do_after == None else do_after
    return GenericTask.objects.create(est_time_to_complete=est_time,
                                      time_created = time_assigned,
                                      scheduled = False,
                                      location = location,
                                      completed = False,
                                      do_after = do_after,
                                      deadline = deadline,
                                      task_description=task_description,
                                      task_name=task_name)

def add_new_task(request,year, month, day):
    print(str(request.POST))
    print("Hello world")
    
    deadline_year = int(request.POST['end_time'][:4])
    deadline_month = int(request.POST['end_time'][5:7])
    deadline_day = int(request.POST['end_time'][8:10])
    deadline_hr = int(request.POST['end_time'][11:13])
    deadline_min = int(request.POST['end_time'][14:16])
    
    #create_generic_task()
    return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))
    #return HttpResponseRedirect(reverse('calendarauto:calendar_view',args=(year, month,day)))#'calendarauto:calendarauto', args=(year, month,day)))
