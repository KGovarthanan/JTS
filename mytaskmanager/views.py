from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from .models import TaskManager
from .forms import TaskForm
from django.db.models import Count
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # print(reverse('home',args=[name]))
            task = TaskManager.objects.values('author').annotate(entry=Count('id'))
            dtask= []
            dauthor = []
            for tasks in task: 
                entry = tasks['entry']
                autask = tasks.get('author')
                client = User.objects.filter(id=autask)
                ntask=TaskManager.objects.filter(author=tasks.get('author'))
                dtask.extend(ntask)
                dauthor.extend(client)
            return render(request,'home.html',{'tasks':dtask,'authors':dauthor,})
        else:
            home = TaskManager()
            return render(request,'home.html',{'tasks':home.view_all_tasks(author = request.user),'author':request.user,'uhome':True})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)
    
def task(request,id):
    if request.user.is_authenticated:
        onetask = TaskManager()
        if request.user.is_superuser:  
            task = TaskManager.objects.values('author').annotate(entry=Count('id'))
            dtask= []
            dauthor = []
            for tasks in task: 
                autask = tasks.get('author')
                client = User.objects.filter(id=autask)
                ntask=TaskManager.objects.filter(author=tasks.get('author'))
                dtask.extend(ntask)
                dauthor.extend(client)
            return render(request,'home.html',{'task':onetask.get_task_by_id(id=id),'authors':dauthor,'author':request.user,'vtask':True})
        return render(request,'home.html',{'task':onetask.get_task_by_id(id=id)})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)
        
def dropdowns(request,name):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            task = TaskManager.objects.values('author').annotate(entry=Count('id'))
            dtask= []
            dauthor = []
            for tasks in task: 
                entry = tasks['entry']
                autask = tasks.get('author')
                client = User.objects.filter(id=autask)
                ntask=TaskManager.objects.filter(author=tasks.get('author'),priority=name)
                dtask.extend(ntask)
                dauthor.extend(client)
            entry =TaskManager.objects.filter(author_id__in=[autask],priority=name)
            return render(request,'home.html',{'tasks':dtask,'authors':dauthor,'search':True,'query':name,'vtask':False})
        return render(request,'home.html',{'tasks':TaskManager().filter_tasks_by_priority(pr=name,author=request.user),'uhome':True, 'search':True,'query':name})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)    
    
def new_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  
            def find_task():
                obj = TaskManager.objects.last()
                tasktitle = f'ID:"{obj.id}"--Title:"{obj.title}"'
                return tasktitle
            form = TaskForm(request.POST)
            if form.is_valid():   
                form.cleaned_data['author']=request.user
                tform = form.cleaned_data
                task = TaskManager()
                task.add_task(**tform)
                task.save()
                mid = find_task()
                if request.user.is_superuser:
                    task = TaskManager.objects.values('author').annotate(entry=Count('id'))
                    dtask= []
                    dauthor = []
                    for tasks in task: 
                        autask = tasks.get('author')
                        client = User.objects.filter(id=autask)
                        ntask=TaskManager.objects.filter(author=tasks.get('author'),)
                        dtask.extend(ntask)
                        dauthor.extend(client)
                    return render(request,'home.html',{'tasks':dtask,'authors':dauthor,'newsave':True,'tasktitle':mid,'author':request.user})
                    # return render(request,'home.html',{'tasks':TaskManager.objects.all().order_by('author'),'newsave':True,'tasktitle':mid,'author':request.user})
                return render(request,'home.html',{'newsave':True,'tasktitle':mid,'tasks':task.view_all_tasks(author=request.user),'author':request.user,'uhome':True})
            else:
                return render(request,'addtask.html',{'form':form})
        else:
            form = TaskForm()
            return render(request,'addtask.html',{'form':form})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)
        
def update_task(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':    
            form = TaskForm(request.POST)
            if form.is_valid():
                form.cleaned_data['id']=id
                form.cleaned_data['author']=request.user
                tform = form.cleaned_data
                obj = get_object_or_404(TaskManager, id=id,)
                tasktitle = f'ID:"{obj.id}"--Title:"{obj.title}"'
                task = TaskManager()
                task.edit_task(tform)
                if request.user.is_superuser:
                    task = TaskManager.objects.values('author').annotate(entry=Count('id'))
                    dtask= []
                    dauthor = []
                    for tasks in task: 
                        autask = tasks.get('author')
                        client = User.objects.filter(id=autask)
                        ntask=TaskManager.objects.filter(author=tasks.get('author'),)
                        dtask.extend(ntask)
                        dauthor.extend(client)
                    return render(request,'home.html',{'tasks':dtask,'authors':dauthor,'save':True,'tasktitle':tasktitle,'author':request.user})
                    # return render(request,'home.html',{'tasks':TaskManager.objects.all().order_by('author'),'save':True,'tasktitle':tasktitle,'author':request.user})
                return render(request,'home.html',{'save':True,'tasktitle':tasktitle,'tasks':task.view_all_tasks(author=request.user),'author':request.user,'uhome':True})
            else:
                task = TaskManager()
                gtask = task.get_task_by_id(id=id)   
                errors = form.errors
                form = TaskForm(instance=gtask)
                return render(request,'update.html',{'form':form,'task':gtask,'errors':errors})
        else:
            task = TaskManager()
            gtask = task.get_task_by_id(id=id)
            form = TaskForm(instance=gtask)
            return render(request,'update.html',{'form':form,'task':gtask})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url) 
       
def del_task(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            task = TaskManager()
            obj = get_object_or_404(TaskManager, id=id)
            tasktitle = f'ID:"{obj.id}"--Title:"{obj.title}"'
            task.delete_task(id=id)
            if request.user.is_superuser:
                task = TaskManager.objects.values('author').annotate(entry=Count('id'))
                dtask= []
                dauthor = []
                for tasks in task: 
                    autask = tasks.get('author')
                    client = User.objects.filter(id=autask)
                    ntask=TaskManager.objects.filter(author=tasks.get('author'),)
                    dtask.extend(ntask)
                    dauthor.extend(client)
                return render(request,'home.html',{'tasks':dtask,'authors':dauthor,'delete':True,'tasktitle':tasktitle,'author':request.user})
                # return render(request,'home.html',{'tasks':TaskManager.objects.all().order_by('author'),'delete':True,'tasktitle':tasktitle,'author':request.user})
            return  render(request,'home.html',{'delete':True,'tasktitle':tasktitle,'tasks':task.view_all_tasks(author=request.user),'author':request.user,'uhome':True})
        else:
            task = TaskManager()
            return render(request,'home.html',{'task':task.get_task_by_id(id=id)})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)
    
def search(request):
    if request.user.is_authenticated:
        query = request.GET.get('search','')
        if query.isdigit() :
            result = TaskManager.objects.filter(id__contains=int(query) ) & TaskManager.objects.filter(author=request.user)
        else:
            result = TaskManager.objects.filter(title__icontains=query ) & TaskManager.objects.filter(author=request.user)
        if request.user.is_superuser:
                task = TaskManager.objects.values('author').annotate(entry=Count('id'))
                dtask= []
                dauthor = []
                for tasks in task: 
                    autask = tasks.get('author')
                    client = User.objects.filter(id=autask)
                    ntask=TaskManager.objects.filter(author=tasks.get('author'),)
                    dtask.extend(ntask)
                    dauthor.extend(client)
                if query.isdigit() :
                    result = TaskManager.objects.filter(id__contains=int(query)  )
                else:
                    result = TaskManager.objects.filter(title__icontains=query ) 
                return render(request,'home.html',{'tasks':result,'authors':dauthor,'search':True,'query':query,}) 
        return render(request,'home.html',{'tasks':result,'uhome':True,'query':query})
    else:
        url = reverse('Mylogin')
        return HttpResponseRedirect(url)
