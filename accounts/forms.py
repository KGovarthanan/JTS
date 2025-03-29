from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,UserChangeForm
from django.contrib.auth.models import User
from django import forms
# from .models import CustomUser

class RegisterForm(UserCreationForm):
    email= forms.EmailField(required=True,label='Your Email',error_messages={"required":"Enter valid Email",},
                            help_text="Enter valid Email",widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email ID'}),
                            )
    first_name = forms.CharField(required=True,label='Your First Name',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your First Name'}),
                                 error_messages={"required":"Enter First Name"})
    username = forms.CharField(required=True,label='Your username',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    last_name = forms.CharField(required=False,label='Your Last Name',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Last Name'}))
    password1 = forms.CharField(required=True,label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),error_messages={"required":"Password missing",})
    password2 = forms.CharField(required=True,label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Renter your password'}),error_messages={"required":"Confirm Password missing",})
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2'] 
        
class LoginForm(AuthenticationForm):
    username = UsernameField(
        required=True,
        label="Your Username", 
        widget=forms.TextInput(attrs={'class': 'form-control ', 'placeholder': 'Enter your username'}),
        error_messages={'required':'Username required'}
    )
    password = forms.CharField(
        required=True,
        label="Your Password",  
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        error_messages={'required':'Password required'}
    )



# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", "phone_number", "age")

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email", "phone_number", "age")
