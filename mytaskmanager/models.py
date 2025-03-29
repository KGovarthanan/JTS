from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Task(models.Model):
    prchoices = [ ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),]
    stchoice = [ ('P', 'Pending'),
        ('I', 'Inprogress'),
        ('C', 'Completed'),]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,null=True)
    description = models.TextField(max_length=2000,null=True)
    priority = models.CharField(choices=prchoices,max_length=50,default='L')
    status = models.CharField(choices=stchoice,max_length=50,default='P')
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    time = models.CharField(null=True,max_length=50)

   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self):
       return f'{self.id}-{self.title}' 

   
class TaskManager(Task,models.Model):
    task = Task.objects.all()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def add_task(self,**args,):
        print("user args :",args)
        self.title = args['title']
        self.description = args['description']
        self.priority = args['priority']
        self.status = args['status']
        self.author = args['author']
        self.time = args['time']
        return Task(self.title,self.description,self.priority,self.status,self.author)
    def get_task_by_id(self,id):
        task = TaskManager.objects.get(id=id)
        return task
    def view_all_tasks(self,author):
        task = TaskManager.objects.filter(author=author)
        return task
    def filter_tasks_by_priority(self,pr,author):
       query =  TaskManager.objects.filter(priority=pr,author=author)
       return query
    def edit_task(self,args):
        print(args)
        obj=TaskManager.objects.filter(id=args['id']).update(
        title=args['title'], 
        description=args['description'], 
        priority=args['priority'], 
        status=args['status'],
        time = args['time']
                )
        return obj
    def delete_task(self,id):
        obj=TaskManager.objects.filter(id=id).delete()
        return obj