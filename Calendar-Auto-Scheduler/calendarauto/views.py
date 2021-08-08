from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.contrib import messages
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
    
    data = serializers.serialize("json", GenericHourBlock.objects.all())
    
    #if (list(GenericTask.objects.values())):
    #    print(list(GenericTask.objects.values()))
    # Function ifInvalidInfo
    # Call the functionsend_user_invalid_input
    
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
    return timezone.make_aware(datetime.datetime(year=year, month=month, day=day, hour=hr, minute=minute))

# Repeat this function until the returned unscheduled task list
# equals the previous returned unscheduled task list.
def schedule_new_task(task):
    # First, try to fit the task in any of the existing hourblocks before the 
    # deadline of this task. return True if this works.
    hourblocks_before_deadline = GenericHourBlock.objects.filter(datetime_gte = timezone.make_aware(datetime.now()), datetime__lt = task.deadline)
    for block in hourblocks_before_deadline:
        block.schedule(task)
        if task.scheduled:
            return True
    
    # We know there wasn't enough space before the task deadline now
    # for this task. get all the hourblocks after the task deadline.
    # We will try to RESCHEDULE SCHEDULED TASKS to these blocks now.
    hourblocks_after_deadline = list(GenericHourBlock.objects.filter(datetime_gte = task.deadline,
                                                                     isFilled=False))
    
    # For each hourblock before the deadline of the task (in reverse
    # order), find out of it can be scheduled in any of the blocks remaining
    # in the unscheduled list. Reschedule it as far out as possible
    # to make more reschedulings possible.
    
    for block in hourblocks_before_deadline[::-1]:
        j = len(hourblocks_after_deadline) - 1
        while j >= 0:
            if hourblocks_after_deadline[j].schedule(block.current_task):
                block.unschedule()
                block.schedule(task)
                return True        
            j -= 1
    
    # If none of the blocks could get rescheduled to later,
    # But one can be done later, unschedule the block with the furthest
    # out deadline, replace that with the task, and return the now 
    # unscheduled 
    hourblock_furthest_deadline = list(GenericHourBlock.objects.filter(
        datetime_gte = timezone.make_aware(datetime.now()), 
        datetime__lt = task.deadline).order_by('current_task__deadline'))[-1]
    if hourblock_furthest_deadline.current_task.deadline > task.deadline:
        furthest_out_deadline_task = hourblock_furthest_deadline.unschedule()
        if hourblock_furthest_deadline.schedule(task):
            return furthest_out_deadline_task
    
    # return all remaining unscheduled tasks.
    # Function breakpoint analysis:
        #   There is an opening before the task deadline
        #   And after the hourblock do_after:
        #       Expected: Schedules the given task. No rescheduling.
        #   There are no openings after the task deadline.
        #       Expected: No reschedulings occur. Task is returned.
        #   There are openings after the task deadline, but no openings
        #   before the task deadline
        #       Expected: System attempts to reschedule 1 hourblock before
        #       task deadline to an hourblock after the task deadline.
        #       Returns nothing.
        #   There are no openings before the task deadline and no openings
        #   after the task deadline, but one task before task deadline
        #   Can be done later.:
        #       Expected: System unschedules the latest task that can be 
        #       Done later, schedules the current task for the now open
        #       hour block, and returns the now unscheduled task.
        #   There are no openings before the task deadline, no openings
        #   After the task deadline, and no tasks that have deadlines
        #   after the task deadline.
        #       Expected: Just returns the task we tried to schedule.
    return task

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
    tasks = []
    for i in range(0, int(task_duration) + 1):
        print('saving task')
        task = create_generic_task(deadline, 1 if i < int(task_duration) else task_duration % 1, do_after=do_after,
                        task_name = request.POST['task_name'] + ('(' + str(i + 1) + '/' + str(int(task_duration) + 1) + ')' if task_duration > 1 else ''),
                        task_description=request.POST['task_desc'])
        task.save()
        tasks.append(task)
    current_datetime = timezone.make_aware(datetime.datetime.now())
    to_schedule = GenericHourBlock.objects.filter(datetime__gte = current_datetime, isFilled = False)
    
    # Schedule a task. 
    # If the task 
    for i in to_schedule: # Should probably automatically spread the task out
                            # across available days... TODO
                            # First, fix the deadline issue.
        i.populate()
        print(i)
        
    # Issue: If all the blocks between the current moment and the deadline of a new task
    # are filled, we can't effectively schedule the task.
    # If there are currently scheduled tasks that have deadline after this tasks',
    # unschedule them and reschedule them to a later time.
    
    # all of the tasks have the same deadline.
    deadline = tasks[0].deadline
    # Get all the hour blocks between the present moment and the task deadline.
    # (Reschedule as far out as possible so that we have enough time to complete)
    # only reschedule blocks that have a task with a deadline after
    # The new task's deadline
    hour_blocks = list(GenericHourBlock.objects.filter(datetime__gte = current_datetime, datetime__lt = deadline, current_task__deadline__gt = deadline).order_by('-datetime'))
    now_unscheduled_tasks = [] # The tasks we unscheduled from hour blocks to make room for the new tasks
    # Reverse order so we do first parts first and last parts last.
    j = len(hour_blocks)-1
    for task in tasks[::-1]:
        if j == -1:
            UserAlerts.send_alert("You are overbooked until " + str(deadline) + ". You need to add more task slots before this time.", request, year, month, day) # Future version, specify the task type too
            break
        # If the task is currently not scheduled, 
        if not task.scheduled:
            # Reschedule the last block we can to this task, and we will reschedule
            # impacted task later.
            unscheduled_task = hour_blocks[j].unschedule()
            now_unscheduled_tasks.append(unscheduled_task)
            hour_blocks[j].schedule(task)
            UserAlerts.send_alert("Rescheduled" + str(unscheduled_task.task_name))
            j -= 1
    # Reschedule any tasks that got moved around due to the deadline conflict
    hour_blocks = list(GenericHourBlock.objects.filter(datetime__gte = deadline, isFilled = False))
    for task in now_unscheduled_tasks:
        for block in hour_blocks:
            if block.schedule(task):
                break
        UserAlerts.send_alert('We rescheduled ' + str(task.task_name) + ", but there isn't enough room to fit its deadline. Add room that fits this task!")
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

# Function for unscheduling a task that is currently attached to the GenericHourBlock
# input (request, year, month, day, GenericHourBlock object/index)

# Function for changing the hour block type of a GenericHourBlock object
# input (request, year, month, day, GenericHourBlock object/index)


class UserAlerts:
    def send_user_invalid_input(input_string, request, year, month, day):
        messages.add_message(request, messages.INFO, input_string)
        
        return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))

    
    def send_alert(alert_string, request, year, month, day):
        messages.add_message(request, messages.INFO, alert_string)
        messages.add_message(request, messages.INFO, 'second message')
        
        #return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day)))
    
    def alert_ask_for_permission(alert, options, request, year, month, day):
        messages.add_message(request, messages.INFO, alert, extra_tags='options')
        return HttpResponseRedirect(reverse('calendarauto:calendar_view', args=(year, month, day), kwargs={'options': 'options'}))
