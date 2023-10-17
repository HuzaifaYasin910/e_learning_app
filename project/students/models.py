from django.contrib.auth.models import User
from django.db import models
from instructors.models import Course,Module



class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,null=False,blank=True)
    last_name = models.CharField(max_length=30,null=False,blank=True)
    profile_image = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    courses_enrolled = models.ManyToManyField(Course, related_name='enrolled_students') 
    completed_modules = models.ManyToManyField(Module, blank=True)
    courses_liked = models.ManyToManyField(Course, blank=True )
    def __str__(self):
        return self.user.username