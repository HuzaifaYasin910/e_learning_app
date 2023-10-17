from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from instructors.models import Instructor,Category
from instructors.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from students.models import Student
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def home(request):
    if request.user.is_authenticated :
        return redirect('/profile/')
    random_courses = Course.objects.all().order_by('?')[:8]
    return render(request,'home/home.html',{'random_courses':random_courses})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            if not request.user.is_superuser:
                return redirect('/profile/')
                pass
            else:
                return redirect('/admin/')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home:login')
    return render(request, 'home/login.html')

# Create your views here.
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def accounts(request):
    accounts = Instructor.objects.all()
    print(accounts)
    return render(request,'home/accounts.html',{'accounts':accounts})



def courses(request):
    
    courses = Course.objects.all()
    return render(request,'home/courses.html',{'courses':courses,"start":True})




def course_class(request,module_id):
    
    module = get_object_or_404(Module, pk=module_id)
    return render(request,'home/course_class.html',{'module':module})


def mark_module_completed(request):
    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        print(module_id)
   
    return HttpResponse("completed")

def logout_view(request):
    logout(request)
    return redirect('/home')



@login_required
def profile(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
        enrolled_courses = student.courses_enrolled.all()
        courses_liked = student.courses_liked.all()

        return render(request,"students/student_prof.html",{"enrolled_courses":enrolled_courses,"courses_liked":courses_liked})
    except Student.DoesNotExist:
        # User is not a student
        pass

    try:
        instructor = user.instructor
        courses = Course.objects.filter(author=instructor)
        categories = Category.objects.all()
        return render(request,"instructors/instructor_prof.html",{'courses':courses,'categories':categories})
    except Instructor.DoesNotExist:
        # User is not an instructor
        pass
    
def about(request):
    return render(request,'home/about.html')
def ourhero(request):
    return render(request,'home/mimi.html')
