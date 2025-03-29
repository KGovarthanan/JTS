from django.core.management.base import BaseCommand
from mytaskmanager.models import Task,TaskManager
from django.contrib.auth.models import User
import getpass

class Command(BaseCommand):
    help = "Manage tasks from the command line"

    def add_arguments(self, parser):

        parser.add_argument("action", type=str, choices=["list", "add", "update","delete"], help="Action to perform")
        parser.add_argument("-i","--task_id", type=int, help="Task ID to update (for updating)")
        # parser.add_argument("user",type=str, help="User ID of the task author (for adding)")
        parser.add_argument("-t","--title", type=str, help="Title of the task (for adding/updating)")
        parser.add_argument("-d","--description", type=str, help="Description of the task")
        parser.add_argument("-p","--priority", type=str, choices=["L", "M", "H"], help="Priority of the task",default='L')
        parser.add_argument("-s","--status", type=str, choices=["P", "I", "C"], help="Status of the task",default='P')
       
        

    def handle(self, *args, **options):
        try:
            print("##### Enter Your Credentials to process your Task #####")
            username = input('Enter Username for Task Manager: ')
                
            password = getpass.getpass("Enter Password: ")
            user = User.objects.get(username=username)
            
            while True:
               
                check = user.check_password(password)
                
                if check:
                        action = options["action"]
                        if action == "list":
                            tasks = TaskManager.objects.filter(author=user.id)
                            if tasks.exists():
                                for task in tasks:
                                    priorities = "Low" if task.priority == "L" else "Medium" if task.priority == "M" else "High"
                                    statuses = "Pending" if task.status == "P" else "InProgress" if task.status == "I" else "Completed ."
                                    print(statuses)
                                    self.stdout.write(self.style.SUCCESS(f"\nTask ID:{task.id} -- Title: {task.title}, Descripition:{task.description}, (Priority: {priorities}, Status: {statuses})".title()))
                            else:
                                self.stdout.write(self.style.WARNING(f"No Task available for {user.username},Kinldy create"))
                            
                        elif action == "add":
                            title = options.get("title")
                            description = options.get("description", "")
                            priority = options.get("priority", "L")
                            status = options.get("status", "P")
                            author_id = user

                            if not title :
                                self.stderr.write("Error: --title required to add a task.")
                                
                            else:
                                
                                task = TaskManager.objects.create(
                                    title=title,
                                    description=description,
                                    priority=priority,
                                    status=status,
                                    author=author_id
                                )
                                
                                self.stdout.write(self.style.SUCCESS(f"Task '{task.title}' added successfully!"))
                    

                        elif action == "update":
                            if user.id == 1 :
                                tasks = TaskManager.objects.all()
                            else: 
                                tasks = TaskManager.objects.filter(author_id=user.id)
                                
                            task_id = options.get("task_id")
                            if not task_id:
                                count = 1    
                                for yourtask in tasks:  
                                    alltask = f"{count}. Task Task ID: {yourtask.id} Task title: {yourtask.title} "
                                    self.stdout.write(self.style.SUCCESS(f"{alltask}")) 
                                    count = count + 1
                                self.stdout.write(self.style.WARNING(f"choose \'Task Id \' from above Tasks list \n")) 
                                self.stderr.write("Error: --task_id is required to update a task.")
                                return

                            try:
                                task = TaskManager.objects.get(id=task_id)
                                if options.get("title"):
                                    task.title = options["title"]
                                if options.get("description"):
                                    task.description = options["description"]
                                if options.get("priority"):
                                    task.priority = options["priority"]
                                if options.get("status"):
                                    task.status = options["status"]
                                
                                task.author = user
                                task.save()
                                self.stdout.write(self.style.SUCCESS(f"Task {task_id}-{task.title},{task.status} updated successfully!"))
                            except TaskManager.DoesNotExist:
                                
                            
                                self.stderr.write(f"Error: Task with ID {task_id} not found.")

                        elif action == "delete":
                            if user.id == 1 :
                                tasks = TaskManager.objects.all()
                            else: 
                                tasks = TaskManager.objects.filter(author_id=user.id)
                                
                            task_id = options.get("task_id")
                            if not task_id:
                                count = 1    
                                for yourtask in tasks:  
                                    alltask = f"{count}. Task Task ID: {yourtask.id} Task title: {yourtask.title} "
                                    self.stdout.write(self.style.SUCCESS(f"{alltask}")) 
                                    count = count + 1
                                self.stdout.write(self.style.WARNING(f"choose \'Task Id \' from above Tasks list \n")) 
                                self.stderr.write("Error: --task_id is required to delete a task.")
                                return

                            try:
                                task = TaskManager.objects.get(id=task_id)
                                task.delete()
                                self.stdout.write(self.style.SUCCESS(f"Task {task_id}-{task.title} deletd successfully!"))
                            except Task.DoesNotExist:
                                self.stderr.write(f"Error: Task with ID {task_id} not found.")

                        break
                else:
                    self.stderr.write(self.style.ERROR("Incorrect password. Try again!"))
                    password = getpass.getpass("Enter Password: ")        
            
            
        except User.DoesNotExist:
            self.stderr.write("Error: Invalid User.")
            
        
   

                    
        
     


 