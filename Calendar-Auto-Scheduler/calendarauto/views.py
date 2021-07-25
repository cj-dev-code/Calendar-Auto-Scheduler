from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
#from datetime import datetime, time
import datetime

from .models import GenericTask, GenericHourBlock

# If the url is going to use varibles, then they must be listed here
# in the function name if it is a custom view i.e. what we have here
def CalendarView(request, year, month, day):
    isValidDate = True
    try:
        datetime.datetime(year, month, day)
    except:
        isValidDate = False
        
    if (isValidDate):
        today = datetime.datetime(year, month, day)
    else:
        today = datetime.datetime.now()
        
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    sat = today + datetime.timedelta(6 - idx)
    return render(request, 'calendarauto/calendar.html', {'sunday' : sun, 'saturday' : sat, 'day' : day})
    
class TodoView(generic.ListView):
    template_name = 'calendarauto/todolist.html'
    context_object_name = 'task_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return GenericTask.objects.order_by('-deadline')

    
def MysteryView(request):
    return render(request, 'calendarauto/calendar.html')
    
def create_generic_task(deadline, hours_to_complete,
                    completed=False,scheduled=False, time_created=None, location='Default',
                    task_name='Default', task_description='Default',
                    do_after = None):
    est_time = datetime.time(int(hours_to_complete), int((hours_to_complete % 1)*60), 0)
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

def get_datetime_from_post(post_string):
    year = int(post_string[:4])
    month = int(post_string[5:7])
    day = int(post_string[8:10])
    hr = int(post_string[11:13])
    minute = int(post_string[14:16])
    return datetime.datetime(year=year, month=month, day=day, hour=hr, minute=minute)

def add_new_task(request,year, month, day):
    print(str(request.POST))
    print("Hello world")
    
    # Always get the time from the datetime function for the deadline
    do_after = get_datetime_from_post(request.POST['start_time'])
    deadline = get_datetime_from_post(request.POST['end_time'])
    task_duration = float(request.POST['duration'])
    
    # make sure the user didn't put an illegal time in.
    if datetime.timedelta(hours=task_duration // 1, minutes=int((task_duration % 1)*60))+ do_after > deadline:
        print('invalid.')
        return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))
    
    
    task = create_generic_task(deadline, task_duration, do_after=do_after,
                        task_name = request.POST['task_name'],
                        task_description=request.POST['task_desc'])
    task.save()
    print('attempted to save task')
    return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))

def schedule_hour_block(request, year, month): 
    # Find the hour block associated with this hour.
        # if it doesn't exist, then make a new one.
    
    # Call the populate method on the hour block.
    day = request['DAY']
    try:
        print(GenericHourBlock.get_hour(day, month, year, day))
    except:
        newblock = GenericHourBlock(datetime=datetime.datetime(year=year, month=month, day=day, hour=day))
        newblock.save()
    return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))