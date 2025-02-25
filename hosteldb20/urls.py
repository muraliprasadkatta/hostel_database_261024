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

from django.contrib.sitemaps.views import sitemap
from hostelapp20.sitemaps import StaticViewSitemap  # Update with your app name if needed
from django.views.generic import TemplateView


# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,  # StaticViewSitemap ni ikkada include chestunnaru
}

app_name = 'hostelapp20'

urlpatterns = [
    path('pwa/', include('pwa.urls')),  # PWA functionality

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),  # Set to the root level
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),name="robots_file"),

    path('admin/', admin.site.urls),
    path('', views.login_and_registration, name='login_and_registration'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_mobile/', views.check_mobile, name='check_mobile'),
    path('check_roomnumber/', views.check_roomnumber, name='check_roomnumber'),
    path('logout/', views.Logout, name='logout'),
    path('addproperty', views.addproperty, name='addproperty'),

    path('property_profile/<int:property_id>/', views.propertyProfile, name='propertyProfile'),

    path('set_management_pin/',views.set_management_pin, name='set_management_pin'),


    path('AddRooms/<int:property_id>', views.AddRooms, name='AddRooms'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('DisplayRooms/<int:property_id>/', views.DisplayRooms, name='DisplayRooms'),
    path('DisplayBeds/<int:property_id>/<int:room_number>/', views.DisplayBeds, name='DisplayBeds'),

    path('AddTenants/<int:property_id>/<int:room_number>/', views.AddTenants, name='AddTenants'),
    
    path('AddTenants/<int:property_id>/<int:room_number>/<int:tenant_id>/', views.AddTenants, name='AddTenants'),

    path('EditTenant/<int:property_id>/<int:room_number>/<int:tenant_id>/', views.EditTenant, name='EditTenant'),


    path('TenantDetails/<int:property_id>/<int:room_number>/<int:tenant_id>/', views.TenantDetails, name='TenantDetails'),
    path('Payments/<int:property_id>/dues/', views.dues_view, name='dues_url'),
    path('Payments/<int:property_id>/remainder/', views.remainder_view, name='remainder_url'),
    path('Payments/<int:property_id>/history/', views.history_view, name='history_url'),
    path('Payments/<int:property_id>/pay/', views.record_payment, name='record_payment'),
    path('DeleteTenant/<int:tenant_id>', views.DeleteTenant, name='DeleteTenant'),
    path('test', views.test, name='test'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('redirectpage', views.redirectpage, name='redirectpage'),

    # This is forgot passwod otp
    path('send-otp/', views.send_otp, name='send_otp'),

    path('validate-otp/',views.validate_otp, name='validate_otp'),

    
    path('set-new-password/',views.set_new_password, name='set_new_password'),


    path('search/',views. search_view, name='search_view'),

    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),

    path('recent-searches/', views.recent_searches, name='recent_searches'),


        # API URLs
    path('api/', include('hostelapp20.api.urls')),  # Including API URLs from the 'api' folder


    path('save_selected_hostel/', views.save_selected_hostel, name='save_selected_hostel'),


    path('upload_image/', views.upload_image, name='upload_image'),

    # urls.py

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)