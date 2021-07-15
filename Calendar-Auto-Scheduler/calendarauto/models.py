from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class GenericTask(models.Model):
    task_name = models.CharField(max_length=100, default = "None")
    task_description = models.CharField(max_length=300,default='None')
    deadline = models.DateTimeField('Deadline')
    do_after = models.DateTimeField('Do After', default=timezone.now) # Do the task by 
    est_time_to_complete = models.TimeField("est. time to complete") # Est time to complete
    completed = models.BooleanField(default=False) # Whether the task is completed or not
    location = models.CharField(max_length = 300) # The location of the task
    scheduled = models.BooleanField(default=False) # Whether the task is scheduled or not

    time_created = models.DateTimeField("Time Created", default=timezone.now)
    # Regulate so that the est task length can't be longer than the difference between
    # Do by and the deadline
    
    def __str__(self):
        return self.task_name + self.task_description 
    

    def get_starting_deadline(self):
        return self.deadline - timedelta(hours = self.est_time_to_complete.hour)
    class Meta:
        get_latest_by = 'time_created'
        
class GenericHourBlock(models.Model):
    hour_type = models.CharField(max_length=2, default='BL') # The type of the hour
    datetime = models.DateTimeField('Hour Representative')
    isFilled = models.BooleanField(default=False)
    current_task = models.ForeignKey(GenericTask, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.hour_type + str(self.get_current_task())
    def populate(self):
        options = GenericTask.objects.all()
                                                    # if it starts before the block ends, it's an option!
        selection = [x.id for x in options if (x.do_after <= self.datetime + timedelta(hours=1) and self.datetime <= x.get_starting_deadline())]
        refined_options = options.filter(id__in = selection)
        if len(refined_options):
            self.current_task = refined_options.earliest()
        
    def get_current_task(self):
        if hasattr(self, 'current_task'):
            return self.current_task
        else:
            return None
    
