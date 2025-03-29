from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
# Create your views here.
def register(request):
    auth_logout(request)
    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        lform = LoginForm(request)
        if form.is_valid():
            myname = form.save()
            print('username',myname)
            auth_logout(request)
            return render(request,'login.html',{'form':lform,'username':myname,'save':True})
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})

def Mylogin(request):
    if request.user.is_authenticated:
        url = reverse('fhome')
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':  
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    url = reverse('fhome')
                    return HttpResponseRedirect(url)
                else:
                    print(form)
                    return render(request,'login.html',{'form':form})
        else:
            form = LoginForm(request)
        return render(request,'login.html',{'form':form})
def auth_logout(request):
    logout(request)
    url = reverse('Mylogin')
    return HttpResponseRedirect(url)
