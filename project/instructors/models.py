from django.contrib.auth.models import User
from django.db import models




class Instructor(models.Model):
    
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=30,null=False,blank=True)
    last_name   = models.CharField(max_length=30,null=False,blank=True)
    bio         = models.TextField()
    profile_image = models.ImageField(upload_to='instructor_profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    



    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Course(models.Model):                                     
    title = models.CharField(max_length=30)
    image  = models.ImageField(upload_to='Course_thumbnails/', null=False)                  
    description = models.TextField(max_length=1500)
    requirements = models.TextField()
    wyl = models.TextField()
    category = models.ManyToManyField(Category)
    students = models.PositiveIntegerField(null=True,blank=True)
    updated_at = models.DateField(auto_now=True,blank=True)
    created_at = models.DateField(auto_now_add=True,blank=True)
    author = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(max_length=1500,blank=True, null=True)
    author = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='contents/')

    def __str__(self):
        return self.title
