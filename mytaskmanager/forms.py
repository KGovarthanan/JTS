from django import forms
from .models import Task,TaskManager
class TaskForm(forms.ModelForm):
    prchoices = [ ('L', 'Low'),
                ('M', 'Medium'),
                ('H', 'High'),]
    stchoice = [ ('P', 'Pending'),
                ('I', 'Inprogress'),
                ('C', 'Completed'),]
    title = forms.CharField(required=True,label='Task Title',min_length=8,max_length=50,label_suffix=":",
                            error_messages={"required":"not to be empty",'min_length':'Must be minimum 8 Chars'},
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(required=False,max_length=200,label_suffix=":",label='Task Description',
                                  widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "style": "resize: none; max-width: 100%; overflow: auto;"}))
    priority = forms.ChoiceField(choices=prchoices,label_suffix=":",label='Task Priority',widget=forms.Select(attrs={"class": "dropdown-item"}),
                                 help_text='Default is Low ,need please change')
    status = forms.ChoiceField(choices=stchoice,label_suffix=":",label='Task status',widget=forms.Select(attrs={"class": "dropdown-item"}),
                               help_text='Default is Pending ,need please change')
    time = forms.CharField(required=True,label="Enter Task duration",label_suffix=":",widget=forms.TextInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = TaskManager
        fields = ['id','title','description','priority','status','time']
