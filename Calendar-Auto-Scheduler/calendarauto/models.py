from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.timezone import make_aware

# Create your models here.

class GenericTask(models.Model):
    task_name = models.CharField(max_length=100, default = "None")
    task_description = models.CharField(max_length=300,default='None')
    deadline = models.DateTimeField('Deadline', null=True)
    do_after = models.DateTimeField('Do After', default=timezone.now, null=True) # Do the task by 
    est_time_to_complete = models.TimeField("est. time to complete") # Est time to complete
    completed = models.BooleanField(default=False) # Whether the task is completed or not
    location = models.CharField(max_length = 300) # The location of the task
    scheduled = models.BooleanField(default=False) # Whether the task is scheduled or not

    time_created = models.DateTimeField("Time Created", default=timezone.now)
    # Regulate so that the est task length can't be longer than the difference between
    # Do by and the deadline
    
    def __str__(self):
        return self.task_name + self.task_description + ". Due by " + str(self.deadline) + ". Start by " + str(self.do_after) + ". Duration: " + str(self.est_time_to_complete)

    def get_starting_deadline(self):
        if (self.deadline != None):
            return make_aware(datetime.max - timedelta(days=365))
        return self.deadline - timedelta(hours = self.est_time_to_complete.hour)
    class Meta:
        get_latest_by = 'time_created'
        
class GenericHourBlock(models.Model):
    hour_type = models.CharField(max_length=2, default='BL') # The type of the hour
    datetime = models.DateTimeField('Hour Representative')
    isFilled = models.BooleanField(default=False)
    current_task = models.ForeignKey(GenericTask, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.hour_type + str(self.get_current_task())
    
    def is_hour(self, day, month, year, hour_start):
        return self.datetime.day == day and self.datetime.month == month and self.datetime.year == year and self.datetime.hour == hour_start
    
    # 
    '''
    Function to get the GenericHourBlock associated with this day, month, and year, and hour start.
    Assumes:
            0 < month < 13
            0 < day < 32
            0 <= hour < 23
            1 <= year <= 9999
    '''
    def get_hour(day, month, year, hour_start):
        
        objects = GenericHourBlock.objects.order_by('-datetime')
        # Binary search this list until you get to the Generic Hour Block.
        target = make_aware(datetime(hour=hour_start, month=month, year=year, day=day ))
        i = 0
        j = len(objects)
        while i < j:
            mid = (i + j)//2
            print(objects[mid].datetime, target,objects[mid].datetime < target )
            if objects[mid].datetime < target:
                j = mid - 1
            elif objects[mid].datetime > target:
                i = mid + 1
            else:
                return objects[mid]
        return None
    
    def populate(self):
        options = GenericTask.objects.all()
                                                    # if it starts before the block ends, it's an option!
        selection = [x.id for x in options if (x.do_after <= self.datetime + timedelta(hours=1) and self.datetime <= x.get_starting_deadline())]
        refined_options = options.filter(id__in = selection)
        if len(refined_options):
            self.current_task = refined_options.earliest()
        if self.get_current_task() == None:
            for i in options:
                if i.do_after == None or i.deadline == None:
                    self.current_task = i
        self.save()
        
    def get_current_task(self):
        if hasattr(self, 'current_task'):
            return self.current_task
        else:
            return None
    
    
