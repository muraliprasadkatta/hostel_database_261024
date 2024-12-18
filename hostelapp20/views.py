
from datetime import datetime, timedelta, date
from calendar import monthrange, isleap
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError, transaction, models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Count, Sum, Max, F
from django.contrib import messages
from django.template.loader import render_to_string   # for ajax to reload the page and block duplication sections
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal
from social_django.models import UserSocialAuth
from django.core.mail import send_mail
import logging
import re
import json
from uuid import uuid4

# Import models
from .models import History, Tenant, Remainder, Room, AddProperty, ManagementPin, CustomUser, ChangedPassword

# Import custom helpers


# def base(request):
#     print("User is authenticated:", request.user.is_authenticated)  # Debugging output
#     if request.user.is_authenticated:
#         user_properties = AddProperty.objects.filter(user=request.user)
#         return render(request, 'base.html', {'user_properties': user_properties})
#     else:
#         print("Redirecting to login because user is not authenticated.")
#         return redirect('login')




def normalize_mobile_number(mobile):
    if mobile.startswith('+91'):
        mobile = mobile[3:]
    return mobile.strip()




@never_cache
def login_and_registration(request):
    show_signup = request.GET.get('show_signup', 'false')  # Default to 'false' to show the login form

    if request.session.get('first_visit', True):
        request.session['first_visit'] = False
        context = {
            'show_signup': 'true',  # Show the registration form by default on the first visit
            'username': '',
            'email': '',
            'mobile': '',
            'password': '',
            'confirmPassword': ''
        }
    else:
        context = {
            'show_signup': show_signup,  # Use the query parameter to decide which form to show
            'username': '',
            'email': '',
            'mobile': '',
            'password': '',
            'confirmPassword': ''
        }

    if request.method == 'POST':
        if 'login' in request.POST:
            identifier = request.POST.get('identifier')
            password = request.POST.get('password')
            user, username = None, None

            # Normalize mobile number if it's a digit
            if identifier.isdigit():
                identifier = normalize_mobile_number(identifier)

            # Determine if identifier is email or mobile number or username
            if '@' in identifier:
                try:
                    user = get_user_model().objects.get(email=identifier)
                    username = user.username
                except get_user_model().DoesNotExist:
                    messages.error(request, 'Invalid email or password.', extra_tags='login_error')
            elif identifier.isdigit():
                try:
                    user = get_user_model().objects.get(mobile_number=identifier)
                    username = user.username
                except get_user_model().DoesNotExist:
                    messages.error(request, 'Invalid mobile number or password.', extra_tags='login_error')
            else:
                try:
                    user = get_user_model().objects.get(username=identifier)
                    username = user.username
                except get_user_model().DoesNotExist:
                    messages.error(request, 'Invalid username or password.', extra_tags='login_error')

            if username:
                user = authenticate(request, username=username, password=password)
                if user:
                    django_login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid username, email, or mobile number, or password.')

            if not user:
                return render(request, 'registration/registrationpage.html')
            pass

        elif 'signup' in request.POST:
            context['show_signup'] = 'false'  # Ensure the signup form remains visible after form submission

            username = request.POST.get('username')
            email = request.POST.get('email').strip() if request.POST.get('email').strip() else None
            mobile = request.POST.get('mobile').strip() if request.POST.get('mobile').strip() else None
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')

            # Ensure email field is reset correctly to avoid concatenation
            if email:
                context['email'] = email
            else:
                context['email'] = ''

            # Update context with the received values to repopulate the form
            context.update({
                'username': username,
                'email': email,
                'mobile': mobile,
                'password': password,
                'confirmPassword': confirm_password
            })

            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.', extra_tags='signup_error')
                return render(request, 'registration/registrationpage.html', context)

            # Check for existing username, email, or mobile number
            username_exists = get_user_model().objects.filter(username=username).exists()
            email_exists = get_user_model().objects.filter(email=email).exists() if email else False
            mobile_exists = get_user_model().objects.filter(mobile_number=mobile).exists() if mobile else False

            if username_exists:
                if email_exists and mobile_exists:
                    messages.error(request, 'This username, email, and mobile are already in use.', extra_tags='signup_error')
                elif email_exists:
                    messages.error(request, 'This username and email are already in use.', extra_tags='signup_error')
                elif mobile_exists:
                    messages.error(request, 'This username and mobile are already in use.', extra_tags='signup_error')
                else:
                    messages.error(request, 'This username is already in use.', extra_tags='signup_error')
                return render(request, 'registration/registrationpage.html', context)

            elif email_exists:
                if mobile_exists:
                    messages.error(request, 'This email and mobile are already in use. Please log in.', extra_tags='signup_error')
                else:
                    messages.error(request, 'This email is already in use. Please log in.', extra_tags='signup_error')

                return render(request, 'registration/registrationpage.html', context)

            elif mobile_exists:
                messages.error(request, 'This mobile number is already in use. Please log in.', extra_tags='signup_error')

                return render(request, 'registration/registrationpage.html', context)

            # Ensure no duplicate check is performed twice
            if username_exists or email_exists or mobile_exists:
                return render(request, 'registration/registrationpage.html', {
                    'username': username,
                    'email': email,
                    'mobile': mobile,
                    'show_signup': True,  # Tell the template to show the signup form
                })

            # Create new user if no conflicts
            user = get_user_model().objects.create_user(username=username, email=email, mobile_number=mobile, password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            django_login(request, user, backend=user.backend)
            return redirect('dashboard')

    # for auto redirect to dashboard page when the applications is close again he open the page its start form dashboard page
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'registration/registrationpage.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# @csrf_exempt
# def save_selected_hostel(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         request.session['selected_hostel_id'] = data.get('property_id')
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'failed'}, status=400)

# views.py
# views.py

def redirectpage(request):
    return render(request,'redirectpage.html')

# views.py

logger = logging.getLogger(__name__)

def Logout(request):
    logout(request)  # This clears the session
    logger.debug("Logged out, redirecting to login.")
    return redirect('login_and_registration')  # Redirect with a query parameter to show the login form


import time

def check_username(request):
    username = request.POST.get('username', '')

    if username:
        time.sleep(0.1)  # Introduce a delay (1 second) to simulate processing time
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse('<div style="color: red;"> This username already exists </div>')
        else:
            return HttpResponse('')  # Return an empty response if the username is available
            # return HttpResponse('<div style="color: green; "> This username is available </div>')  # Return an empty response if the username is available

    else:
        return HttpResponse('')  # Return an empty response if the username field is empty


from django.contrib.auth import get_user_model

def check_email(request):
    email = request.POST.get('email', '').strip()

    if email:
        time.sleep(0.1)  # Introduce a delay to simulate processing time
        if get_user_model().objects.filter(email=email).exists():
            return HttpResponse('<div style="color: red;">This email is already in use</div>')
        else:
            return HttpResponse('')

    else:
        return HttpResponse('')  # Return an empty response if the email field is empty


# Normalize is user for its remove the +91 while checking in data dashboard
def normalize_mobile_number(mobile):
    if mobile.startswith('+91'):
        mobile = mobile[3:]
    return mobile.strip()

def check_mobile(request):
    mobile = request.POST.get('mobile', '').strip()

    if mobile:
        mobile = normalize_mobile_number(mobile)
        time.sleep(0.1)  # Introduce a delay to simulate processing time
        if get_user_model().objects.filter(mobile_number=mobile).exists():
            return HttpResponse('<div style="color: red;">This mobile number is already in use</div>')
        else:
            return HttpResponse('')
    else:
        return HttpResponse('')  # Return an empty response if the mobile field is empty



def check_roomnumber(request):
    roomnumber = request.POST.get('roomnumber', '')
    property_id = request.POST.get('property_id', '')  # Retrieve property_id from the request
    user = request.user  # Retrieve the currently logged-in user


    if roomnumber:
        time.sleep(0.1)  # Simulate processing time
        # Adjust the filter to include property_id
        if Room.objects.filter(user=user, room_number=roomnumber, property_id=property_id).exists():
            return HttpResponse('<div style="color: red;">This room number already exists</div>')
        else:
            return HttpResponse('')
    else:
        return HttpResponse('')  # Return an empty response if the room number field is empty



from cloudinary.uploader import upload  # Ensure this import if not already

def addproperty(request):
    user = request.user
    pin_exists = ManagementPin.objects.filter(user=user).exists()

    if request.method == 'POST':
        hostelname = request.POST.get('hostelname')
        ownername = request.POST.get('ownername')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image = request.FILES.get('image')

        if user.is_authenticated:
            if not pin_exists:
                managementPin = request.POST.get('managementPin')
                ManagementPin.objects.create(user=user, pin=managementPin)

            existing_property = AddProperty.objects.filter(
                hostelname=hostelname,
                ownername=ownername,
                email=email,
                mobile=mobile,
                address=address,
                user=user
            ).first()

            if existing_property:
                messages.warning(request, 'Property with the same details already exists.')
            else:
                # Upload image to Cloudinary and print the URL
                if image:
                    result = upload(image)
                    image_url = result.get('url')
                    print("Cloudinary URL:", image_url)  # Print Cloudinary URL to verify

                    new_property = AddProperty.objects.create(
                        hostelname=hostelname,
                        ownername=ownername,
                        email=email,
                        mobile=mobile,
                        address=address,
                        latitude=latitude,
                        longitude=longitude,
                        user=user,
                        image=image_url  # Save URL instead of the file itself
                    )
                    messages.success(request, 'Property added successfully.')

            return redirect('dashboard')
        else:
            messages.error(request, 'User is not authenticated')

    username = user.username if user.is_authenticated else "Guest"
    user_pin_set = pin_exists if user.is_authenticated else False
    
    return render(request, 'data/addproperty.html', {'user_pin_set': user_pin_set})




def set_management_pin(request):
    if request.method == 'POST':
        managementPin = request.POST.get('managementPin')
        
        # Ensure PIN is valid and unique
        if ManagementPin.objects.filter(user=request.user).exists():
            messages.error(request, 'PIN already set.')
        else:
            ManagementPin.objects.create(user=request.user, pin=managementPin)
            messages.success(request, 'Management PIN set successfully.')

        return redirect('add_property')



@never_cache
def dashboard(request):
    if request.user.is_authenticated:
        selected_hostel_id = request.session.get('selected_hostel_id')
        if selected_hostel_id:
            return redirect('DisplayRooms', property_id=selected_hostel_id)

        user_properties = AddProperty.objects.filter(user=request.user)
        
        # Get PIN information
        pin_exists = ManagementPin.objects.filter(user=request.user).exists()
        management_pin = ManagementPin.objects.filter(user=request.user).first()
        management_pin_value = management_pin.pin if management_pin else None

        return render(request, 'dashboard.html', {
            'user_properties': user_properties,
            'user_pin_set': pin_exists,
            'username': request.user.username,
            'management_pin_value': management_pin_value
        })
    else:
        return redirect('login_and_registration')  # Redirect to login page if the user is not authenticated




def AddRooms(request, property_id):
    print(f"AddRooms view called with property_id: {property_id}")

    selected_property = get_object_or_404(AddProperty, id=property_id, user=request.user)

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room_number = request.POST.get('roomnumber')
        floor_type = request.POST.get('floortype')
        number_of_share = int(request.POST.get('numberofshare'))
        available_room_or_not = request.POST.get('available_room_or_not')
        remarks = request.POST.get('remarks')
        room_facilities = request.POST.getlist('transportation')
        current_occupied_beds = request.POST.get('current_occupied_beds', '0')  # Default to '0' if not present

        # Convert room facilities list to a comma-separated string
        room_facilities_str = ', '.join(room_facilities)

        # Convert current_occupied_beds to an integer, with a default value of 0 if conversion fails
        try:
            current_occupied_beds = int(current_occupied_beds)
        except ValueError:
            current_occupied_beds = 0

        # Check if the room number already exists for the selected property, excluding the current room if it's being edited
        if room_id:
            existing_room = Room.objects.filter(property_id=property_id, room_number=room_number, user=request.user).exclude(id=room_id).first()
        else:
            existing_room = Room.objects.filter(property_id=property_id, room_number=room_number, user=request.user).first()

        if existing_room:
            return JsonResponse({'success': False, 'error': f'Room number {room_number} already exists. Please enter a unique room number.'})

        # If room_id exists, it means we are editing an existing room
        if room_id:
            room = get_object_or_404(Room, id=room_id, user=request.user)
            # Backend validation
            if number_of_share < current_occupied_beds:
                return JsonResponse({'success': False, 'error': f'The number of beds cannot be less than the currently occupied beds ({current_occupied_beds}).'})

            # Update room details
            room.room_number = room_number
            room.floor_type = floor_type
            room.number_of_share = number_of_share
            room.available_room_or_not = available_room_or_not
            room.remarks = remarks
            room.room_facilities = room_facilities_str
            room.save()
            return JsonResponse({'success': True, 'message': 'Room updated successfully.'})
        else:
            # Create a new room instance and save it
            room = Room(
                property=selected_property,
                user=request.user,
                room_number=room_number,
                floor_type=floor_type,
                number_of_share=number_of_share,
                available_room_or_not=available_room_or_not,
                remarks=remarks,
                room_facilities=room_facilities_str
            )
            room.save()
            return JsonResponse({'success': True, 'message': 'Room added successfully.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})




@never_cache
def DisplayRooms(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    
    # Print statement to debug in development environment
    # get the properties of images of profile section in sidebar
    if selected_property.image:
        selected_property.image_url = selected_property.image.url.replace("/http%3A/", "http://")
    else:
        selected_property.image_url = None
        
    # Other code remains the same
    user_properties = AddProperty.objects.filter(user=request.user)

    # get the properties of images of properties in sidebar
    for property in user_properties:
        if property.image:
            property.image_url = property.image.url.replace("/http%3A/", "http://")
        else:
            property.image_url = None
            
    user_rooms = Room.objects.filter(user=request.user, property=selected_property).annotate(
        has_data=Count('tenant')
    ).order_by('room_number')
    
    # Convert room data to list for use in JavaScript
    user_rooms_list = list(user_rooms.values(
        'id', 'room_number', 'floor_type', 'number_of_share', 
        'available_room_or_not', 'remarks', 'room_facilities', 'has_data'
    ))
    user_rooms_json = json.dumps(user_rooms_list, cls=DjangoJSONEncoder)

    # Room and bed statistics
    total_rooms = user_rooms.count()
    total_beds = user_rooms.aggregate(total_beds=Sum('number_of_share'))['total_beds'] or 0
    occupied_beds = Tenant.objects.filter(room__in=user_rooms).count()
    free_beds = total_beds - occupied_beds

    context = {
        'username': request.user.username,
        'selected_property': selected_property,
        'user_properties': user_properties,
        'user_rooms': user_rooms,
        'user_rooms_json': user_rooms_json,
        'total_rooms': total_rooms,
        'occupied_beds': occupied_beds,
        'free_beds': free_beds,
        'show_change_property_button': True,
    }

    return render(request, 'data/display_rooms.html', context)


from cloudinary.uploader import upload  # Ensure this import if not already

def AddTenants(request, property_id, room_number, tenant_id=None):
    print(f"AddTenants view called for property: {property_id}, room: {room_number}, tenant: {tenant_id}")

    selected_property = get_object_or_404(AddProperty, id=property_id)
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    associated_user = room.user
    tenant = None

    if tenant_id:
        tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        adhar_number = request.POST.get('adhar_number')
        govt_id_front = request.FILES.get('govt_id_front')
        govt_id_back = request.FILES.get('govt_id_back')
        state = request.POST.get('state')
        dist = request.POST.get('dist')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        door_no = request.POST.get('door_no')
        area = request.POST.get('area')
        street = request.POST.get('street')
        landmark = request.POST.get('landmark')
        bike_number = request.POST.get('bike_number')
        joining_date = request.POST.get('joining_date')
        allocated_bed = request.POST.get('allocated_bed')
        rent = request.POST.get('rent')
        advance = request.POST.get('advance')
        tenant_image = request.FILES.get('tenant_image')

        # Upload images to Cloudinary if present
        if govt_id_front:
            govt_id_front_url = upload(govt_id_front).get('url')
        else:
            govt_id_front_url = tenant.govt_id_front if tenant else None

        if govt_id_back:
            govt_id_back_url = upload(govt_id_back).get('url')
        else:
            govt_id_back_url = tenant.govt_id_back if tenant else None

        if tenant_image:
            tenant_image_url = upload(tenant_image).get('url')
        else:
            tenant_image_url = tenant.tenant_image if tenant else None

        if tenant:
            # Update existing tenant
            tenant.name = name
            tenant.email = email
            tenant.mobile = mobile
            tenant.adhar_number = adhar_number
            tenant.govt_id_front = govt_id_front_url
            tenant.govt_id_back = govt_id_back_url
            tenant.state = state
            tenant.dist = dist
            tenant.pincode = pincode
            tenant.city = city
            tenant.door_no = door_no
            tenant.area = area
            tenant.street = street
            tenant.landmark = landmark
            tenant.bike_number = bike_number
            tenant.joining_date = joining_date
            tenant.allocated_bed = allocated_bed
            tenant.rent = rent
            tenant.advance = advance
            tenant.tenant_image = tenant_image_url
        else:
            # Create a new tenant
            tenant = Tenant(
                name=name,
                email=email,
                mobile=mobile,
                adhar_number=adhar_number,
                govt_id_front=govt_id_front_url,
                govt_id_back=govt_id_back_url,
                state=state,
                dist=dist,
                pincode=pincode,
                city=city,
                door_no=door_no,
                area=area,
                street=street,
                landmark=landmark,
                bike_number=bike_number,
                joining_date=joining_date,
                allocated_bed=allocated_bed,
                rent=rent,
                advance=advance,
                tenant_image=tenant_image_url,
                room=room,
                property=selected_property,
                user=associated_user
            )
        tenant.save()

        # Return a JSON response to indicate success
        return JsonResponse({'success': True, 'message': 'Tenant added/updated successfully.'})

    if request.method == 'GET':
        form_html = render_to_string('data/add_tenants_modal.html', {
            'selected_property': selected_property,
            'room': room,
            'associated_user': associated_user,
            'tenant': tenant,
        })
        return JsonResponse({'form_html': form_html})





from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Tenant, Room, AddProperty

def EditTenant(request, property_id, room_number, tenant_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    tenant = get_object_or_404(Tenant, id=tenant_id)

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        adhar_number = request.POST.get('adhar_number')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        dist = request.POST.get('dist')
        city = request.POST.get('city')
        door_no = request.POST.get('door_no')
        area = request.POST.get('area')
        street = request.POST.get('street')
        landmark = request.POST.get('landmark')
        bike_number = request.POST.get('bike_number')
        joining_date = request.POST.get('joining_date')
        allocated_bed = request.POST.get('allocated_bed')
        rent = request.POST.get('rent')
        advance = request.POST.get('advance')

        # Handle image upload
        tenant_image = request.FILES.get('tenant_image')

        # Update tenant details
        tenant.name = name
        tenant.email = email
        tenant.mobile = mobile
        tenant.adhar_number = adhar_number
        tenant.pincode = pincode
        tenant.state = state
        tenant.dist = dist
        tenant.city = city
        tenant.door_no = door_no
        tenant.area = area
        tenant.street = street
        tenant.landmark = landmark
        tenant.bike_number = bike_number
        tenant.joining_date = joining_date
        tenant.allocated_bed = allocated_bed
        tenant.rent = rent
        tenant.advance = advance

        # Update tenant image if a new one is uploaded
        if tenant_image:
            tenant.tenant_image = tenant_image

        # Save the tenant details
        tenant.save()

        # Redirect to a success page or tenant details page
        return redirect('TenantDetails', property_id=property_id, room_number=room_number, tenant_id=tenant_id)

    # If the request method is not POST, render the tenant details page
    return render(request, 'data/tenant_details.html', {
        'room': room,
        'tenant': tenant,
        'selected_property': selected_property,
    })




def DisplayBeds(request, property_id, room_number):
    selected_property = get_object_or_404(AddProperty, id=property_id)

    # Format the image URL for selected_property
    # get the properties of images of profile section in sidebar
    if selected_property.image:
        selected_property.image_url = selected_property.image.url.replace("/http%3A/", "http://")
    else:
        selected_property.image_url = None

    # Get room and tenant information
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    beds = Tenant.objects.filter(room=room)

    user_properties = AddProperty.objects.filter(user=request.user)
    # get the properties of images of properties in sidebar
    for property in user_properties:
        if property.image:
            property.image_url = property.image.url.replace("/http%3A/", "http://")
        else:
            property.image_url = None

    remaining_free_beds = room.number_of_share - beds.count()
    current_date = timezone.now().date()

  
    context = {
        'selected_property': selected_property,
        'room': room,
        'beds': beds,
        'remaining_free_beds': remaining_free_beds,
        'user_properties': user_properties,

    }

    return render(request, 'data/display_beds.html', context)


def TenantDetails(request, property_id, room_number, tenant_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)

        # Format the image URL for selected_property
    if selected_property.image:
        selected_property.image_url = selected_property.image.url.replace("/http%3A/", "http://")
    else:
        selected_property.image_url = None
        
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    tenant = get_object_or_404(Tenant, id=tenant_id)

    # Include additional tenant details in the context if they're available in your model
    context = {
        'room': room,
        'tenant': tenant,
        'selected_property': selected_property,
        'email': tenant.email,  # Assuming this field exists in your Tenant model
        'mobile': tenant.mobile,  # Assuming this field exists in your Tenant model
        'adhar_number': tenant.adhar_number,  # Example
        'pincode': tenant.pincode,  # Example
        'state': tenant.state,  # Example
        'dist': tenant.dist,  # Example
        'city': tenant.city,  # Example
        'door_no': tenant.door_no,  # Example
        'area': tenant.area,  # Example
        'street': tenant.street,  # Example
        'landmark': tenant.landmark,  # Example
        'bike_number': tenant.bike_number,  # Example
        'joining_date': tenant.joining_date,  # Example
        'allocated_bed': tenant.allocated_bed,  # Example
        'rent': tenant.rent,  # Example
        'advance': tenant.advance,  # Example
        'tenant_image': tenant.tenant_image,  # Example
    }

    return render(request, 'data/tenant_details.html', context)



def DeleteTenant(request, tenant_id):
    # First, retrieve the tenant object from the database
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    property_id = tenant.room.property_id
    room_number = tenant.room.room_number
    
    # Perform the deletion
    tenant.delete()
    
    # After deletion, prepare to redirect to avoid re-deletion issues
    # Setup the no-cache headers
    # ('DisplayBeds', property_id=property_id, room_number=room_number)
    response = redirect(reverse('DisplayBeds', args=(property_id, room_number)))

    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
    response['Pragma'] = 'no-cache'  # HTTP 1.0.
    response['Expires'] = '0'  # Proxies.


    # Return the response to redirect the user and avoid caching of the redirect
    return response






def Payments(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)

    context = {
        'selected_property': selected_property,
        # Add other context data as needed
    }
    return redirect('dues_url', property_id=property_id)



def dues_view(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)
     # Print statement to debug in development environment
    if selected_property.image:
        selected_property.image_url = selected_property.image.url.replace("/http%3A/", "http://")
    else:
        selected_property.image_url = None

    user_properties = AddProperty.objects.filter(user=request.user)

    # get the properties of images of properties in sidebar
    for property in user_properties:
        if property.image:
            property.image_url = property.image.url.replace("/http%3A/", "http://")
        else:
            property.image_url = None

    date_str = request.GET.get('date')
    
    if date_str:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        date_filtered = True
        tenants_with_due_today = Tenant.objects.filter(
            property=selected_property, 
            next_due_date=selected_date
        ).exclude(remainder__isnull=False)
    else:
        selected_date = timezone.now().date()
        date_filtered = False
        tenants_with_due_today = Tenant.objects.filter(
            property=selected_property, 
            next_due_date__lte=selected_date
        ).exclude(remainder__isnull=False)

    context = {
        'selected_property': selected_property,
        'tenants_with_due_today': tenants_with_due_today,
        'selected_date': selected_date,
        'date_filtered': date_filtered,
        'user_properties':user_properties
    }
    return render(request, 'collections/sections/dues.html', context)




@csrf_protect
def remainder_view(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    user_properties = AddProperty.objects.filter(user=request.user)


    if request.method == 'POST':
        tenant_id = request.POST.get('tenant_id')
        amount_paid = request.POST.get('amount_paid')
        remaining_amount = request.POST.get('remaining_amount')
        payment_type = request.POST.get('payment_type')
        reference_number = request.POST.get('reference_number')
        payment_screenshot = request.FILES.get('payment_screenshot')

        if not tenant_id or not amount_paid or not remaining_amount:
            return redirect('remainder_url', property_id=property_id)

        try:
            tenant = Tenant.objects.get(id=tenant_id)

            # Always create a new history record for every payment
            History.objects.create(
                tenant=tenant,
                amount_paid=Decimal(amount_paid),
                payment_method=payment_type,
                payment_reference=reference_number if payment_type == 'online' else None,
                payment_screenshot=payment_screenshot if payment_type == 'screenshot' else None
            )

            if Decimal(remaining_amount) == 0:
                # If the remaining amount is 0, delete the remainder and update the due date
                Remainder.objects.filter(tenant=tenant).delete()
                tenant.next_due_date += relativedelta(months=1)  # Correctly adding one month
                tenant.save()
            else:
                try:
                    remainder = Remainder.objects.get(tenant=tenant)
                    # Update the existing remainder
                    remainder.amount_paid += Decimal(amount_paid)
                    remainder.remaining_amount = Decimal(remaining_amount)
                    remainder.payment_type = payment_type
                    remainder.reference_number = reference_number
                    remainder.payment_screenshot = payment_screenshot
                    remainder.due_date = tenant.next_due_date
                    remainder.save()
                except Remainder.DoesNotExist:
                    # Create a new remainder
                    Remainder.objects.create(
                        tenant=tenant,
                        amount_paid=Decimal(amount_paid),
                        remaining_amount=Decimal(remaining_amount),
                        payment_type=payment_type,
                        reference_number=reference_number,
                        payment_screenshot=payment_screenshot,
                        due_date=tenant.next_due_date,
                        
                    )

        except Tenant.DoesNotExist:
            pass  # Handle the error as needed
        except Exception as e:
            pass  # Handle the error as needed

        return redirect('remainder_url', property_id=property_id)

    remainders = Remainder.objects.filter(tenant__property=selected_property)
    context = {
        'selected_property': selected_property,
        'remainders': remainders,
        'user_properties':user_properties

    }
    return render(request, 'collections/sections/remainder.html', context)


def history_view(request, property_id):
    histories = History.objects.filter(tenant__property_id=property_id).select_related('tenant')
    return render(request, 'collections/sections/history.html', {'histories': histories})



def record_payment(request, property_id):
    if request.method == 'POST':
        tenant_id = request.POST.get('tenant_id')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_type')
        payment_reference = request.POST.get('reference_number')
        payment_screenshot = request.FILES.get('payment_screenshot')

        if tenant_id is None or amount is None or payment_method is None:
            return HttpResponse("Invalid data", status=400)

        tenant = get_object_or_404(Tenant, id=tenant_id)

        try:
            amount = Decimal(amount)
            tenant_rent = Decimal(tenant.rent)
        except ValueError:
            return HttpResponse("Invalid amount or tenant rent", status=400)

        try:
            # Always create a new history record for every payment
            History.objects.create(
                tenant=tenant,
                amount_paid=amount,
                payment_method=payment_method,
                payment_reference=payment_reference if payment_method == 'online' else None,
                payment_screenshot=payment_screenshot if payment_method == 'screenshot' else None
            )

            # Check if the full rent amount is paid
            if amount >= tenant_rent:
                # Calculate the next due date
                if tenant.next_due_date:
                    tenant.next_due_date += relativedelta(months=1)
                else:
                    tenant.next_due_date = tenant.joining_date + relativedelta(months=1)

                tenant.save()

                # Remove any existing remainder if full rent is paid
                Remainder.objects.filter(tenant=tenant).delete()
            else:
                # Update or create a remainder record for partial payments
                try:
                    remainder = Remainder.objects.get(tenant=tenant)
                    remainder.amount_paid += amount
                    remainder.remaining_amount = tenant_rent - remainder.amount_paid
                    remainder.payment_type = payment_method
                    remainder.reference_number = payment_reference
                    remainder.payment_screenshot = payment_screenshot
                    remainder.due_date = tenant.next_due_date
                    remainder.save()
                except Remainder.DoesNotExist:
                    Remainder.objects.create(
                        tenant=tenant,
                        amount_paid=amount,
                        remaining_amount=tenant_rent - amount,
                        payment_type=payment_method,
                        reference_number=payment_reference,
                        payment_screenshot=payment_screenshot,
                        due_date=tenant.next_due_date
                    )

            return HttpResponseRedirect(reverse('dues_url', args=[property_id]))

        except Exception as e:
            return HttpResponse(f"Error processing payment: {e}", status=500)

    return HttpResponse("Invalid request method", status=405)

def test(request):
    return render(request,'test.html')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import AddProperty

# views.py లో

from urllib.parse import unquote
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404

def propertyProfile(request, property_id):
    property = get_object_or_404(AddProperty, id=property_id)
    if property.image:
        property.image_url = property.image.url.replace("/http%3A/", "http://")
    else:
        property.image_url = None
    return render(request, 'baseSidebar/header_property_profile.html', {'property': property})


@csrf_exempt
def save_selected_hostel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_hostel_id'] = data.get('property_id')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)



# views.py
from django.shortcuts import render, redirect
from cloudinary.uploader import upload
from django.conf import settings
from django.http import JsonResponse

# this is for testing purpose we can remove any time  and template too upload_button_template.html
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            result = upload(image)  # Upload image to Cloudinary
            image_url = result.get('url')
            return JsonResponse({"success": True, "image_url": image_url})
    return JsonResponse({"success": False, "error": "Failed to upload image"})





import uuid  # Add this for generating the token
import random
from urllib.parse import urlencode

# here we use the email_helper.py file
import random
import uuid
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import OtpValidation
from hostelapp20.forgot_password_helpers.email_helper import send_otp_email

def send_otp(request):
    """
    Handles OTP generation and sending it via email.
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if email is provided
        if not email:
            return HttpResponse("Email is required!", status=400)

        # Generate OTP and token
        otp = f"{random.randint(100000, 999999)}"
        token = str(uuid.uuid4())  # Generate a unique token

        # Delete old records for the same email (Modification 1)
        OtpValidation.objects.filter(email=email).delete()

        # Save OTP and token in the database
        try:
            OtpValidation.objects.create(email=email, otp=otp, token=token)  # Modification 2
            print(f"Generated OTP: {otp}, Token: {token}")  # Optional: For debugging
        except Exception as e:
            print(f"Error saving OTP and token: {e}")
            return HttpResponse("Error saving OTP to the database.", status=500)

        # Send OTP to the user's email
        response = send_otp_email(email, otp)
        if response.get('success'):
            # Redirect back to the previous page with a success message
            query_params = urlencode({'otp_sent': 'true', 'email': email})
            return redirect(f"{request.META.get('HTTP_REFERER')}?{query_params}")
        else:
            # Return error if email sending fails
            return HttpResponse(f"Error: {response.get('error')}", status=500)

    # If request method is not POST
    return HttpResponse("Invalid request method", status=405)



def validate_otp(request):
    """
    Handles OTP validation logic.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        if not email or not otp:
            return HttpResponse("Both email and OTP are required!", status=400)

        try:
            otp_record = OtpValidation.objects.get(email=email, otp=otp)

            # OTP validated successfully
            if otp_record:
                # Redirect to Set New Password Page with the token
                return redirect(f"/set-new-password/?token={otp_record.token}")
            else:
                return HttpResponse("Invalid OTP!", status=400)
        except OtpValidation.DoesNotExist:
            return HttpResponse("Invalid email or OTP!", status=400)

    return HttpResponse("Invalid request method", status=405)






from django.http import HttpResponse
from django.shortcuts import render
from .models import OtpValidation
from django.contrib.auth import get_user_model

User = get_user_model()  # Reference the custom user model
def set_new_password(request):
    """
    Handles setting a new password for the user.
    """
    if request.method == 'GET':
        # Fetch the token from the query parameters
        token = request.GET.get('token')

        if not token:
            return HttpResponse("Token is required!", status=400)

        # Fetch the OTP record using the token
        try:
            otp_record = OtpValidation.objects.get(token=token)
        except OtpValidation.DoesNotExist:
            return HttpResponse("Invalid token!", status=400)

        # Render the password reset form with the email
        return render(request, 'registration/verification_codes/set_new_password_modal.html', {'email': otp_record.email})

    elif request.method == 'POST':
        # Handle password update logic
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not email or not new_password or not confirm_password:
            return HttpResponse("All fields are required!", status=400)

        if new_password != confirm_password:
            return HttpResponse("Passwords do not match!", status=400)

        try:
            # Update the user's password
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Clean up OTP records
            OtpValidation.objects.filter(email=email).delete()

            return HttpResponse("Password updated successfully!")
        except User.DoesNotExist:
            return HttpResponse("User does not exist!", status=400)

    return HttpResponse("Invalid request method", status=405)
