# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "students"

urlpatterns = [
    path('mark_module_completed/',mark_module_completed,name='mark_module_completed'),
    path('register_student/',create_student_account,name='register_student'),
    path('enroll/<int:course_id>/',enroll_in_course,name='enroll'),
    path('course_detail/<int:course_id>',course_detail,name='course_detail'),
    path('courses_liked/<int:course_id>',courses_liked,name='courses_liked'),
    path('course_class/<int:module_id>/<int:course_id>/',course_class,name='course_class'),
    path('courses/',courses,name='courses'),
    path('author/<int:author_id>',author,name='author'),
    path('category/<category_id>/<category_name>',category,name='category')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
