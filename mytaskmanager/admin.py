from django.contrib import admin
from .models import Task,TaskManager
# Register your models here.

@admin.register(Task,TaskManager) 
class Taskadmin(admin.ModelAdmin):  
    list_display = ['id','title','description']
    list_display_links = ['id','title']
    list_filter = ['priority','status']
    search_fields = ['title','description']
    

# admin.site.register(TaskManager,Taskadmin)
