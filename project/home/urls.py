from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('home/',home,name='home'),
    path('about/',about,name='about'),
    path('ourhero/',ourhero,name='ourhero'),
    path('login/',login_view,name='login'),
    path('accounts/',accounts,name='accounts'),
    
    path('logout/', logout_view, name='logout'), 
    path('profile/',profile,name='profile')
]
