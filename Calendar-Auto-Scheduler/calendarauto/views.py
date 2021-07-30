from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
#from datetime import datetime, time
import datetime

from .models import GenericTask, GenericHourBlock
import sys


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
<<<<<<< HEAD
    
    data = serializers.serialize("json", GenericHourBlock.objects.all())
    
    if (list(GenericTask.objects.values())):
        print(list(GenericTask.objects.values()))
    
=======
        
>>>>>>> def4e5e8b32cde43c3932f6ba2da249498ee6999
    return render(request, 'calendarauto/calendar.html', {'sunday' : sun, 
                                                          'saturday' : sat, 
                                                          'task_list' : list(GenericTask.objects.values()),
                                                          'hour_blocks' : list(GenericHourBlock.objects.values()),
                                                          'hour_info' : data,
                                                          })
    
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
    est_time = datetime.timedelta(hours=int(hours_to_complete), minutes=int((hours_to_complete % 1)*60))
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
    print(sys._getframe().f_code.co_name)
    
    # Upgrade add_new_task it makes the ceil of duration number of tasks 
    # So that tasks are at most an hour long.
    # Always get the time from the datetime function for the deadline
    do_after = get_datetime_from_post(request.POST['start_time'])
    deadline = get_datetime_from_post(request.POST['end_time'])
    task_duration = float(request.POST['duration'])-.0001
    # make sure the user didn't put an illegal time in.
    if datetime.timedelta(hours=task_duration // 1, minutes=int((task_duration % 1)*60))+ do_after > deadline:
        print('invalid.')
        return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))
    print('attempted to save task')
    for i in range(0, int(task_duration) + 1):
        print('saving task')
        task = create_generic_task(deadline, 1 if i < int(task_duration) else task_duration % 1, do_after=do_after,
                        task_name = request.POST['task_name'] + ('(' + str(i + 1) + '/' + str(int(task_duration) + 1) + ')' if task_duration > 1 else ''),
                        task_description=request.POST['task_desc'])
        task.save()
    return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))

def schedule_hour_block(request, year, month, day): 
    print(sys._getframe().f_code.co_name)
    # Find the hour block associated with this hour.
        # if it doesn't exist, then make a new one.
    # Call the populate method on the hour block.
    # Format the start time from the front end into military time for our generic block
    print(request.POST)
    start_time = request.POST['start_time1']
    if 'pm' in start_time:
        start_time = (int(start_time[:-2]) + 12) % 24
    elif 'am' in start_time:
        start_time = int(start_time[:-2])
        if start_time == 12:
            start_time =0
    else:
        start_time = int(start_time)
        
    # Get the current day from the request
    day = int(request.POST['DAY'])
    
    # And get the hour block associated with that hour (make one if it's not there)
    newBlock = GenericHourBlock.get_hour(day, month, year, start_time)
    print(newBlock)
    if type(newBlock) == type(None):
        newBlock = GenericHourBlock(datetime=timezone.make_aware(datetime.datetime(year=year, month=month, day=day, hour=start_time)))
        #newblock.save()
        print('second call', newBlock)
    newBlock.populate()
    return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))