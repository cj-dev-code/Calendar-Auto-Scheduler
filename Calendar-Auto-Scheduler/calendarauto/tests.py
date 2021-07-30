from django.test import TestCase
# Create your tests here.
#6:43-6:47
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from .models import GenericTask, GenericHourBlock
import sys 

def create_generic_task(deadline, hours_to_complete,
                    completed=False,scheduled=False, time_created=None, location='Default',
                    task_name='Default', task_description='Default',
                    do_after = None):
    est_time = timedelta(hours=int(hours_to_complete), minutes=int((hours_to_complete % 1)*60))
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
    def test_populate_with_do_after_before_block_and_task_deadline_before_block(self):
        print()
        print(sys._getframe().f_code.co_name)
        gtask_deadline = timezone.make_aware(datetime(2021, 7, 10, 12, 0, 0))
        gtask_hrs_to_c = 1
        time_created = timezone.make_aware(datetime(2021, 7, 7, 12, 0, 0))
        #gtask_deadline = timezone.make_aware(time_created)
        #time_created = timezone.make_aware(gtask_deadline)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, time_created=time_created)
        
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 12, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        self.assertIs(hourblock.get_current_task(), None)
    def test_populate_with_do_after_after_block_and_task_deadline_before_block(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Expected Behavior
        # Populates the block.
        
        # Also test multiple after.
        gtask_deadline = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c = .25
        time_created = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after = timezone.make_aware(datetime(2021, 7, 13, 11, 15,0))
        #gtask_deadline = timezone.make_aware(time_created)
        #time_created = timezone.make_aware(gtask_deadline)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, do_after=do_after, time_created=time_created,
                                    task_name = "Test do_after after block start and deadline before block end")
        
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIs(hourblock.get_current_task().id,gtask.id)
        
    def test_populate_with_do_after_before_block_and_task_deadline_after_block(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Expected Behavior
        # Populates the block.
        
        # Also test multiple after.
        gtask_deadline = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c = .25
        time_created = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        #gtask_deadline = timezone.make_aware(time_created)
        #time_created = timezone.make_aware(gtask_deadline)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, do_after=do_after, time_created=time_created,
                                    task_name = "Test do_after before block start and deadline before block end")
        
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIs(hourblock.get_current_task().id,gtask.id)
        
    def test_populate_with_2do_after_before_block_and_task_deadline_before_block(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Expected Behavior
        # Populates the block with the earliest result
        
        # Also test multiple after.
        gtask_deadline = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c = .25
        time_created = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        
        gtask_deadline2 = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c2 = .25
        time_created2 = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after2 = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        #gtask_deadline = timezone.make_aware(time_created)
        #time_created = timezone.make_aware(gtask_deadline)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, do_after=do_after, time_created=time_created,
                                    task_name = "Test do_after before block start and deadline before block end")
        gtask2 = create_generic_task(gtask_deadline2, gtask_hrs_to_c2, do_after=do_after2, time_created=time_created2,
                                    task_name = "Test do_after before block start and deadline before block end2")
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIs(hourblock.get_current_task().id,gtask.id)
        
    def test_populate_with_2do_after_before_block_but_one_valid_deadline(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Expected Behavior
        # Populates the block with the earliest result
        
        # The invalid task.
        gtask_deadline = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c = 2
        time_created = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        
        # The valid task.
        gtask_deadline2 = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c2 = .25
        time_created2 = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after2 = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        #gtask_deadline = timezone.make_aware(time_created)
        #time_created = timezone.make_aware(gtask_deadline)
        gtask = create_generic_task(gtask_deadline, gtask_hrs_to_c, do_after=do_after, time_created=time_created,
                                    task_name = "Test do_after before block start and deadline before block end")
        gtask2 = create_generic_task(gtask_deadline2, gtask_hrs_to_c2, do_after=do_after2, time_created=time_created2,
                                    task_name = "Test do_after before block start and deadline before block end2")
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIs(hourblock.get_current_task().id,gtask2.id)

    def test_populate_set_new_task_to_scheduled(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Get a valid task
        gtask_deadline2 = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c2 = .25
        time_created2 = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after2 = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        
        gtask2 = create_generic_task(gtask_deadline2, gtask_hrs_to_c2, do_after=do_after2, time_created=time_created2,
                                    task_name = "Test do_after before block start and deadline before block end2")
        
        # Make an hour block in that hour
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIs(hourblock.get_current_task().scheduled, True)
        
    def test_populate_wont_double_schedule_a_task(self):
        print()
        print(sys._getframe().f_code.co_name)
        # Get a valid task
        gtask_deadline2 = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c2 = .25
        time_created2 = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after2 = timezone.make_aware(datetime(2021, 7, 13, 10, 15,0))
        
        gtask2 = create_generic_task(gtask_deadline2, gtask_hrs_to_c2, do_after=do_after2, time_created=time_created2,
                                    task_name = "Test do_after before block start and deadline before block end2")
        
        # Make an hour block in that hour
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        # Make an hour block in that hour
        hour_block2_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock2 = create_hour_block(hour_block2_datetime)
        hourblock2.populate()
        
        self.assertIs(hourblock.get_current_task().scheduled, True)
        self.assertIs(hourblock2.get_current_task(), None)
        
    def test_assign_a_task_that_fits_perfectly_in_the_block(self):
        print()
        print(sys._getframe().f_code.co_name)
        
        
        # Make a valid task. 1 hour long between 11a and 12p on July 12, 2021
        gtask_deadline2 = timezone.make_aware(datetime(2021, 7, 13, 12, 0, 0))
        gtask_hrs_to_c2 = 1
        time_created2 = timezone.make_aware(datetime(2021, 7, 12, 12, 0, 0))
        do_after2 = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        taskname = 'Test do_after before block start and deadline before block end2'
        gtask2 = create_generic_task(gtask_deadline2, gtask_hrs_to_c2, do_after=do_after2, time_created=time_created2,
                                    task_name = taskname)
        # Make an hour block in that hour
        hour_block_datetime = timezone.make_aware(datetime(2021, 7, 13, 11, 0,0))
        hourblock = create_hour_block(hour_block_datetime)
        hourblock.populate()
        
        self.assertIn(hourblock.get_current_task().task_name, str(taskname))
        