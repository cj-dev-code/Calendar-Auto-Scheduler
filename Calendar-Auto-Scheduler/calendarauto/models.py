from django.db import models
from django.utils import timezone
# Create your models here.
<<<<<<< HEAD

class GenericTask(models.Model):
    
    task_name = models.CharField(max_length=100)
    task_description = models.CharField(max_length=300)
    deadline = models.DateTimeField('Deadline')
    do_after = models.DateTimeField('Do After', default=timezone.now()) # Do the task by 
    est_time_to_complete = models.TimeField("est. time to complete") # Est time to complete
    completed = models.BooleanField(default=False) # Whether the task is completed or not
    location = models.CharField(max_length = 300) # The location of the task
    scheduled = models.BooleanField(default=False) # Whether the task is scheduled or not

    time_created = models.DateTimeField("Time Created", default=timezone.now())

    def get_starting_deadline(self):
        return self.deadline - self.est_time_to_complete
    
class GenericActiveTask(GenericTask):
    pass
class GenericInactiveTask(GenericTask):
    pass

class GenericHourBlock(models.Model):
    hour_type = models.CharField(max_length=2, default='BL') # The type of the hour
    datetime = models.DateTimeField('Hour Representative')
    isFilled = models.BooleanField(default=False)
    current_task = models.ForeignKey(GenericTask, ondelete=models.CASCADE)
    
    def populate(self):
        options = GenericActiveTask.objects.all()
        selection = [x for ]
        
=======
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField()

    def get_absolute_url(self):
        return reverse('archive_week', kwargs={'pk': self.pk})
>>>>>>> 56435d8 (Added the calendar.html)
