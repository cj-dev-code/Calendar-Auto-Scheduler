from django.test import TestCase
# Create your tests here.
#6:43-6:47
from datetime import timedelta
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import GenericTask, GenericHourBlock

def create_generic_task(deadline, hours_to_complete,
                    completed=False,scheduled=False, time_created=None, location='Default',
                    task_name='Default', task_description='Default',
                    do_after = None):
    est_time = timedelta(hours=hours_to_complete)
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

def create_hour_block(datetime, hour_type = "BL",
                      isFilled=False,
                      current_task = None):
    return GenericHourBlock(datetime = datetime,
                            hour_type = hour_type,
                            isFilled=isFilled,
                            current_task = current_task)

class GenericHourBlockTests(TestCase):
    def test_populate_with_task_deadline_before_hourblock_start(self):
        gtask_deadline = datetime(2021, 7, 10, 12, 0, 0)
        gtask_hrs_to_c = 1
        time_created = datetime(2021, 7, 7, 12, 0, 0)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, time_created=time_created)
        
        hour_block_datetime = datetime(2021, 7, 13, 12, 0,0)
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        print(hourblock.current_task)
        
                

class QuestionModelTests(TestCase):
    '''
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date = time, text='CRABS')
        self.assertIs(old_question.was_published_recently(), True)
    
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=49, seconds=59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)
    '''