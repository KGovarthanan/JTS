from django.core.management.base import BaseCommand
from mytaskmanager.models import Task
from django.contrib.auth.models import User
import getpass

class Command(BaseCommand):
    help = "Create User from the command line"
    
    def handle(self, *args, **options):
 
        username = input('Enter Username for Register: ')
        
       
        while True:
            first_name = input('Enter First Name for Register: ')
            
            if first_name:
                break
            else:
                self.stderr.write(self.style.ERROR("First Name is Must. Try again!"))
        last_name = input('Enter last Name for Register (optional): ')
        while True:
            password1 = getpass.getpass("Enter Password: ")
            password2 = getpass.getpass("Confirm Password: ")
            if password1 :
                if password1 == password2 :
                    break
                else:
                    self.stderr.write(self.style.ERROR(" Passwords do not match. Try again!"))
            else:
                self.stderr.write(self.style.ERROR(" Passwords is missing!"))
                pass

        if User.objects.filter(username=username).exists():
            self.stderr.write(self.style.ERROR(f"Username '{username}' is already exists."))
            return
        
        user = User(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password1)  
        user.save()
        self.stdout.write(self.style.SUCCESS(f"User '{username}' registered successfully!"))