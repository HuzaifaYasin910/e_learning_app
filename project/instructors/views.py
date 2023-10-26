from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from instructors.models import Instructor
from .models import Course, Module
from .forms import UserRegistrationForm,CourseCreationForm,InstructorUpdateForm
from django.views.decorators.cache import cache_control
import mimetypes
from django.urls import reverse






def create_instructor_account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            first_name  = form.cleaned_data['first_name']
            last_name   = form.cleaned_data['last_name']
            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            email       = form.cleaned_data['email']
            bio         = form.cleaned_data['bio']
            profile_image = form.cleaned_data['profile_image']
        try:
            if not username or not email or not password:
                messages.error(request, 'All fields are required.')
                return render(request, 'instructors/register.html')
        except Exception as e:
            messages.error(request, 'please fill in all fields')
            return redirect('/register_instructor/')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            instructor = Instructor(user=user, bio=bio, profile_image=profile_image,first_name=first_name, last_name=last_name)
            instructor.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('/login')
        except IntegrityError:
            messages.error(request, 'A user with the same username or email already exists.')
            return redirect('/register_instructor/')
        except KeyError:
            messages.error(request, 'Invalid form submission. Please try again.')
            return redirect('/register_instructor/')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('/register_instructor/')
    return render(request, 'instructors/register.html')
















@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def create_course(request):
    user = request.user.instructor
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            title       = form.cleaned_data['title']
            image       = form.cleaned_data['image']
            description = form.cleaned_data['description']
            requirements = form.cleaned_data['requirements']
            wyl         = form.cleaned_data['wyl']
            category    = form.cleaned_data['category']  
            print(f"################ COURSE CREATION ##################\nTitle: {title}\nCategory: {category}\n################################")
            new_course  = Course.objects.create(title=title, description=description, requirements=requirements, wyl=wyl, author=user, image=image) 
            new_course.category.set(category) 
            course_id   = new_course.id
            return redirect(f'/course_detail-p/{course_id}/')
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors)  
    return HttpResponse('error')

     

def is_video(file_path):
    content_type, encoding = mimetypes.guess_type(file_path)
    return content_type and content_type.startswith('video/')

def course_class(request, module_id, course_id):
    module = get_object_or_404(Module, pk=module_id)
    course = get_object_or_404(Course, pk=course_id)
    is_video_var = is_video(module.file.url)
    return render(request, 'instructors/class.html', {
        'module': module,
        'course': course,        
        'is_video':is_video_var,
    })









@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def course_detail(request,course_id):
    course = get_object_or_404(Course,pk=course_id)
    return render(request,'instructors/course_detail.html',{'course':course})

def confirm(request,module_id,course_id):
    return render(request,'instructors/confirm.html',{'module_id':module_id,'course_id':course_id})



def delete_module(request,module_id,course_id):
    get_object_or_404(Module,pk=module_id).delete()
    return redirect(f'/course_detail-p/{course_id}')

def add_module(request):
    user = request.user.instructor
    
    if request.method == 'POST':
            print(request.POST)
            course_id  = request.POST.get('course')
            title   = request.POST.get('title')   
            file    = request.FILES.get('file')   
            description = request.POST.get('description')
            course = Course.objects.get(pk=course_id)
            new_module = Module.objects.create(title=title,course=course,author=user,file=file,description=description)
            return redirect(f'/course_class-p/{new_module.id}/{course_id}')
    return HttpResponse('error')






@login_required
def update_instructor_account(request):
    instructor = Instructor.objects.get(user=request.user)
    if request.method == 'POST':
        form = InstructorUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            if 'profile_image' in request.FILES:
                instructor.profile_image = request.FILES['profile_image']
            else:
                instructor.profile_image = instructor.profile_image              
            instructor.first_name = request.POST.get('first_name')
            instructor.last_name = request.POST.get('last_name')
            instructor.bio = request.POST.get('bio')            
            instructor.save()
            return redirect(reverse('home:profile'))
    else:
        form = InstructorUpdateForm(initial={
            'first_name': instructor.first_name,
            'last_name': instructor.last_name,
            'bio': instructor.bio,           
        })
    context = {'form': form, 'instructor': instructor}
    return render(request, 'instructors/update.html', context)



def publish_course(request,course_id):
    Course.objects.filter(pk=course_id).update(published=True)
    return redirect('/profile/')



def enrolled_students(request, course_id):return render(request,'instructors/enrolled_students.html',{'enrolled_students':get_object_or_404(Course, id=course_id).enrolled_students.all()})







