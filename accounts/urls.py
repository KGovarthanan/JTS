from django.urls import path
from accounts import views
from mytaskmanager import views as taskview

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.Mylogin,name='Mylogin'),
    path('logout/',views.auth_logout,name='logout'),
    path('task/home/',taskview.home,name='fhome')
]
