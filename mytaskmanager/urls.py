from django.urls import path
from mytaskmanager import views
from accounts import views as accviews
urlpatterns = [
    path('home/',views.home,name='home'),
    path('<int:id>/',views.task,name='mytask'),
    path('dropdown/<str:name>',views.dropdowns,name='query'),
    path('addtask/',views.new_task,name='newtask'),
    path('update/<int:id>/',views.update_task,name='updatetask'),
    path('delete/<int:id>',views.del_task,name='deletetask'),
    path('register/',accviews.register,name='register'),
    path('login/',accviews.Mylogin,name='Mylogin'),
    path('logout/',accviews.auth_logout,name='logout'),
    path('search',views.search,name='searchbox')
  
   
]
