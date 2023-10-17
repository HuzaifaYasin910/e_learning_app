# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = 'instructors'

urlpatterns = [
        path('register_instructor/',create_instructor_account,name='register_instructor'),
        path('update_instructor/',update_instructor_account,name='update_instructor'),


        path('add_module/',add_module,name='add_module'),
        path('delete_module/<int:module_id>/<int:course_id>/',delete_module,name='delete_module'),
        path('confirm/<int:module_id>/<int:course_id>/',confirm,name='confirm'),
        
        path('create_course/',create_course,name='create_course'),
        path('course_detail-p/<int:course_id>',course_detail,name='course_detail-p'),
        
        path('publish_course/<course_id>',publish_course,name='publish_course'),
        path('course_class-p/<int:module_id>/<int:course_id>/',course_class,name='course_class-p'),

        path('enrolled_students/<course_id>',enrolled_students,name='enrolled_students'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
