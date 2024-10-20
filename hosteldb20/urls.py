"""
URL configuration for hosteldb20 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from hostelapp20 import views 
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static  ## for static or js 
from django.urls import path, include
from django.contrib.auth import views as auth_views


app_name = 'hostelapp20'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_and_registration, name='login_and_registration'),

    # path('',views.Registration, name='registration'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_mobile/', views.check_mobile, name='check_mobile'),

    path('check_roomnumber/', views.check_roomnumber, name='check_roomnumber'),

    # path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),

    path('addproperty',views.addproperty,name='addproperty'),

    path('AddRooms/<int:property_id>',views.AddRooms,name='AddRooms'),
    
    path('dashboard/',views.dashboard,name='dashboard'),

    path('DisplayRooms/<int:property_id>/',views.DisplayRooms,name='DisplayRooms'),

    path('DisplayBeds/<int:property_id>/<int:room_number>/',views.DisplayBeds,name='DisplayBeds'),

    path('AddTenants/<int:property_id>/<int:room_number>/',views.AddTenants,name='AddTenants'),

    path('TenantDetails/<int:property_id>/<int:room_number>/<int:tenant_id>/', views.TenantDetails, name='TenantDetails'),
    

    path('Collections/<int:property_id>/', views.Collections, name='Collections'),


    path('FullPayment/<int:property_id>/',views.FullPayment,name='FullPayment'),

    path('remainder/<int:property_id>/', views.RemainderPage, name='RemainderPage'),

    path('DeleteTenant/<int:tenant_id>',views.DeleteTenant,name='DeleteTenant'),


    path('social-auth/', include('social_django.urls', namespace='social')),

    path('redirectpage',views.redirectpage,name='redirectpage'),


    path('change-password/<str:token>/', views.ChangePassword, name='ChangePassword'),
    path('forget-password/', views.ForgetPassword, name='ForgetPassword'),

    path('test-email/',views.test_email, name='test_email'),


    path('save_selected_hostel/', views.save_selected_hostel, name='save_selected_hostel'),


    # urls.py

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)