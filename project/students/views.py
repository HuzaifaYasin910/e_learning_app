from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Student
from instructors.models import Course,Instructor,Module,Category
from django.http import JsonResponse
import mimetypes
from django.db.models import Q

# Create your views here.







def create_student_account(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'students/register.html')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            instructor = Student(user=user, profile_image=profile_image,first_name=first_name,last_name=last_name)
            instructor.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('/login')
        except IntegrityError:
            messages.error(request, 'A user with the same username or email already exists.')
        except KeyError:
            messages.error(request, 'Invalid form submission. Please try again.')
        except Exception as e:
            print(e)
    return render(request, 'students/register.html')

def enroll_in_course(request, course_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        messages.error(request, 'You have to login first!')
        return redirect('/login')  
    student = request.user.student
    course = get_object_or_404(Course, pk=course_id)
    student.courses_enrolled.add(course)
    return redirect(f'/profile/')


def course_detail(request,course_id):
    course = get_object_or_404(Course,pk=course_id)
    return render(request,'students/course_detail.html',{'course':course})

def courses_liked(request,course_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        messages.error(request, 'You have to login first to enroll or save course')
        return redirect('/login')  
    course = get_object_or_404(Course,pk=course_id)
    student = request.user.student  

    if course in student.courses_liked.all():
        student.courses_liked.remove(course) 
        return JsonResponse({'status':200})
    else:
        student.courses_liked.add(course)
        response_data = {'course_added': True}
        return JsonResponse(response_data)

def is_video(file_path):
    content_type, encoding = mimetypes.guess_type(file_path)
    return content_type and content_type.startswith('video/')

def progress_check(course_id,module_id,student) :
    course = get_object_or_404(Course, pk=course_id)
    course_count = course.module_set.count()
    student_progress_count = student.completed_modules.filter(course=course).count()
    student_progress_percentage = 0
    if course_count > 0:
        student_progress_percentage = int((student_progress_count / course_count) * 100)
        return student_progress_percentage
    else:
        return student_progress_percentage

def mark_module_completed(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        messages.error(request, 'You have to login first!')
        return redirect('/login') 
    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        course_id = request.POST.get('course_id')
        course_count = request.POST.get('course_count')
        module = get_object_or_404(Module, id=module_id)
        student = request.user.student
        if module not in student.completed_modules.all():
            student.completed_modules.add(module)
            student_progress_percentage = progress_check(course_id,module_id,student)
            response_data = {'student_progress_percentage': student_progress_percentage,'status':200}
            return JsonResponse(response_data)
    return JsonResponse({'status':200})

def course_class(request, module_id, course_id):
    student = request.user.student
    module = get_object_or_404(Module, pk=module_id)
    is_video_var = is_video(module.file.url)
    course = get_object_or_404(Course, pk=course_id)
    student_progress_percentage = progress_check(course_id,module_id,student)    
    return render(request, 'students/class.html', {        
        'module': module,
        'course': course,
        'student': student,
        'student_progress': student_progress_percentage,
        'is_video':is_video_var,
    })



def courses(request):
    courses = Course.objects.all().filter(published=True).order_by('?')[:8]
    catagories = Category.objects.all()
    return render(request,'students/categories.html',{'catagories':catagories,'courses':courses,"start":True})

def author(request,author_id):
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        messages.error(request, 'You have to login first!')
        return redirect('/login')  
    author = get_object_or_404(Instructor,pk=author_id)
    return render(request,'students/author.html',{'author':author})

def category(request,category_id,category_name):
    courses = Course.objects.all().filter(category=category_id,published=True)
    return render(request,'students/courses.html',{'courses':courses,'category_name':category_name})


