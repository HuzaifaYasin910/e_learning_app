# forms.py
from .models import Instructor
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User 





class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    bio = forms.CharField(max_length=500, widget=forms.Textarea)
    profile_image = forms.ImageField(required=False)

class CourseCreationForm(forms.Form):
    title = forms.CharField(max_length=30)
    image = forms.ImageField(required=False)
    description = forms.CharField(max_length=1500)
    requirements = forms.CharField()
    wyl = forms.CharField()
    category = forms.CharField()  # Change "catagory" to "category"

    
    




class InstructorUpdateForm(ModelForm):
    class Meta:
        model = Instructor  # Specify the model class here
        fields = ['first_name', 'last_name', 'bio', 'profile_image']

        

