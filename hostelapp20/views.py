
from datetime import datetime, timedelta
from calendar import monthrange, isleap
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login ,logout

from django.http import HttpResponse
from django.db import IntegrityError, models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Max, F
from dateutil.relativedelta import relativedelta
from django.template.loader import render_to_string   # for ajx in while relod the page blck the duplication sctions
from decimal import Decimal
from social_django.models import UserSocialAuth
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.db import transaction

import logging
import re


from .models import CustomUser, AddProperty, Room, Tenant ,PaymentHistory,PaymentRemainder


from django.contrib import messages

# def base(request):
#     print("User is authenticated:", request.user.is_authenticated)  # Debugging output
#     if request.user.is_authenticated:
#         user_properties = AddProperty.objects.filter(user=request.user)
#         return render(request, 'base.html', {'user_properties': user_properties})
#     else:
#         print("Redirecting to login because user is not authenticated.")
#         return redirect('login')



from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib import messages



from django.contrib.auth import get_user_model, login as django_login
from django.shortcuts import redirect
from django.contrib import messages
from django.db import IntegrityError, transaction

@never_cache
def dashboard(request):
    if request.user.is_authenticated:
        selected_hostel_id = request.session.get('selected_hostel_id')
        if selected_hostel_id:
            return redirect('DisplayRooms', property_id=selected_hostel_id)

        user_properties = AddProperty.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'user_properties': user_properties})
    else:
        return redirect('login_and_registration')  # Redirect to login page if the user is not authenticated


from django.contrib.auth import authenticate, login as django_login
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def normalize_mobile_number(mobile):
    if mobile.startswith('+91'):
        mobile = mobile[3:]
    return mobile.strip()


from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache


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
            context['show_signup'] = 'true'  # Ensure the signup form remains visible after form submission

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

@csrf_exempt
def save_selected_hostel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['selected_hostel_id'] = data.get('property_id')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

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



# if it is activated pass the id to the template
#     <div id="passwordError"></div>
# <div id="confirmPasswordError"></div>


# from django.http import HttpResponse
# import json

# def check_passwords(request):
#     password = request.POST.get('password', '')
#     confirm_password = request.POST.get('confirmPassword', '')

#     if password and confirm_password:
#         if password == confirm_password:
#             return HttpResponse(json.dumps({'match': True}), content_type="application/json")
#         else:
#             return HttpResponse(json.dumps({'match': False, 'message': 'Passwords do not match'}), content_type="application/json")
#     return HttpResponse(json.dumps({'match': False, 'message': 'Both password fields are required'}), content_type="application/json")


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

# Login    
@never_cache
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
                new_property = AddProperty.objects.create(
                    hostelname=hostelname,
                    ownername=ownername,
                    email=email,
                    mobile=mobile,
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    user=user,
                    image=image
                )
                messages.success(request, 'Property added successfully.')

            return redirect('dashboard')
        else:
            messages.error(request, 'User is not authenticated')

    username = user.username if user.is_authenticated else "Guest"
    user_pin_set = pin_exists if user.is_authenticated else False
    
    return render(request, 'data/addproperty.html', {'user_pin_set': user_pin_set})




from django.views.decorators.cache import never_cache


from django.http import HttpResponse


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import Room, AddProperty  # Adjust your import according to your actual models
from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import AddProperty, Room
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import AddProperty, Room

def AddRooms(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id, user=request.user)

    if request.method == 'POST':
        room_number = request.POST.get('roomnumber')
        floor_type = request.POST.get('floortype')
        number_of_share = request.POST.get('numberofshare')
        available_room_or_not = request.POST.get('available_room_or_not')
        remarks = request.POST.get('remarks')
        room_facilities = request.POST.getlist('transportation')

        # Convert room facilities list to a comma-separated string
        room_facilities_str = ', '.join(room_facilities)

        # Check if the room number already exists
        if Room.objects.filter(property_id=property_id, room_number=room_number, user=request.user).exists():
            messages.error(request, 'Room number already exists. Please enter a unique room number.')
            return redirect(reverse('DisplayRooms', kwargs={'property_id': property_id}))

        try:
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
            messages.success(request, 'Room added successfully.')
        except Exception as e:
            # Log the error and send a message to the user
            messages.error(request, 'Failed to add room due to an error: {}'.format(str(e)))
            return redirect(reverse('DisplayRooms', kwargs={'property_id': property_id}))

        # Redirect to the room display view or any other appropriate page
        return redirect(reverse('DisplayRooms', kwargs={'property_id': property_id}))

    # Show form if not a POST request or if the form is reloaded freshly
    return render(request, 'data/add_rooms.html', {'property_id': property_id, 'selected_property': selected_property})


from django.db.models import Count, Sum

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest

def DisplayRooms(request, property_id):
    # Retrieve the selected property dashboard on the ID
    selected_property = get_object_or_404(AddProperty, id=property_id)

    # Assuming each user can be associated with multiple properties
    user_properties = AddProperty.objects.filter(user=request.user)

    # Query rooms for the selected property
    user_rooms = Room.objects.filter(user=request.user, property=selected_property).annotate(
        has_data=Count('tenant')
    ).order_by('room_number')

    # Calculate the total number of rooms
    total_rooms = user_rooms.count()

    # Calculate the total number of beds
    total_beds = user_rooms.aggregate(total_beds=Sum('number_of_share'))['total_beds'] or 0

    # Calculate the total number of occupied beds
    occupied_beds = Tenant.objects.filter(room__in=user_rooms).count()

    # Calculate the number of free beds
    free_beds = total_beds - occupied_beds

    if request.method == 'POST':
        # Print POST data if the request method is POST
        print("POST data received:", request.POST)
        
        # Check if essential data is received
        if 'roomnumber' in request.POST:
            print("Room Number Received:", request.POST['roomnumber'])
        else:
            print("Error: No room number received in POST.")
            # You can handle the error by sending a bad request response or by adding an error message in the context
            return HttpResponseBadRequest("Required data not received in POST request.")

    context = { 
        'username': request.user.username,
        'selected_property': selected_property,
        'user_properties': user_properties,
        'user_rooms': user_rooms,
        'some_room_number': user_rooms.first().room_number if user_rooms.exists() else None,
        'total_rooms': total_rooms,
        'occupied_beds': occupied_beds,
        'free_beds': free_beds,
        'error': None  # You can use this to pass error messages to the template
    }
    
    return render(request, 'data/display_rooms.html', context)



def AddTenants(request, property_id, room_number):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)

    # Fetch the user associated with the room
    associated_user = room.user

    if request.method == 'POST':
        # Retrieve form data from POST request
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
        # due_date = request.POST.get('due_date')
        allocated_bed = request.POST.get('allocated_bed')
        rent = request.POST.get('rent')
        advance = request.POST.get('advance')
        tenant_image = request.FILES.get('tenant_image')
        
        # Retrieve associated user ID and room ID from POST request
        room_id = int(request.POST.get('room'))
        
        # Create and save the Tenant object
        tenant = Tenant(
            name=name,
            email=email,
            mobile=mobile,
            adhar_number=adhar_number,
            govt_id_front=govt_id_front,
            govt_id_back=govt_id_back,
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
            # due_date=due_date,
            allocated_bed=allocated_bed,
            rent=rent,
            advance=advance,
            tenant_image=tenant_image,
            room_id=room_id,  # Use room ID from POST
            property=selected_property,
            user=associated_user  # Assign the associated user
        )
        tenant.save()

        # Redirect to the success URL after saving the tenant
        # return redirect(reverse('DisplayRooms', kwargs={'property_id': property_id}))
        return redirect(reverse('DisplayBeds', kwargs={'property_id': property_id, 'room_number': room_number}))
    
    # Render the form with initial data
    return render(request, 'data/add_tenants.html', {'selected_property': selected_property,
                                                      'room': room,
                                                      'associated_user': associated_user})




def monthdelta(date, delta):
    """A simple utility function to add or subtract months from a given date."""
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)



def DisplayBeds(request, property_id, room_number):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    beds = Tenant.objects.filter(room=room)
    user_properties = AddProperty.objects.filter(user=request.user)

    remaining_free_beds = room.number_of_share - beds.count()
    current_date = timezone.now().date()

    for bed in beds:
        past_due_dates = []
        month_count = (current_date.year - bed.joining_date.year) * 12 + current_date.month - bed.joining_date.month

        next_due_date = monthdelta(bed.joining_date, month_count)
        is_today_due_date = current_date == next_due_date

        for month in range(month_count if is_today_due_date else month_count + 1):
            past_due_date = monthdelta(bed.joining_date, month)
            past_due_dates.append(past_due_date)

        if not is_today_due_date:
            next_due_date = monthdelta(bed.joining_date, month_count + 1)

        bed.past_due_dates = past_due_dates
        bed.upcoming_due_date = next_due_date if not is_today_due_date else current_date

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
    room = get_object_or_404(Room, property_id=property_id, room_number=room_number)
    tenant = get_object_or_404(Tenant, id=tenant_id)

    payment_history = PaymentHistory.objects.filter(tenant=tenant).order_by('-date_paid')
    payment_remainders = PaymentRemainder.objects.filter(tenant=tenant).order_by('-date_paid')


    # Initialize variables
    current_date = timezone.now().date()
    past_dues = []
    next_due_date = tenant.joining_date

    # Collect all past due dates
    while next_due_date + relativedelta(months=1) < tenant.due_date:
        next_due_date += relativedelta(months=1)
        if next_due_date <= current_date:
            past_dues.append(next_due_date)
    
    context = {
        'room': room,
        'tenant': tenant,
        'selected_property': selected_property,
        'past_dues': past_dues,  # Pass the list of past dues to the template
        'payment_history': payment_history,
        'payment_remainders' : payment_remainders

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



# Assuming you import your models: AddProperty, Tenant, PaymentHistory, and any other necessary model

def FullPayment(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)

    if request.method == 'POST':
        tenant_id = request.POST.get('tenantId')
        if tenant_id and tenant_id.isdigit():
            tenant = get_object_or_404(Tenant, id=int(tenant_id))
            amount_paid = Decimal(request.POST.get('amount_paid', '0'))
            remaining_amount = request.POST.get('remaining_amount')

            
            # Use 'payment_method_modal' or 'payment_method', depending on which is present
            payment_method = request.POST.get('payment_method_modal', request.POST.get('payment_method', 'cash'))
            reference_id = request.POST.get('reference_id', '') if payment_method == 'refId' else None
            payment_screenshot = request.FILES.get('payment_screenshot', None) if payment_method == 'screenshot' else None

            # Logic to calculate 'remaining_amount' and proceed with creating a PaymentHistory object
            # Assuming you have a method to calculate the total due amount
            total_due_amount = tenant.total_due()
            remaining_amount = max(total_due_amount - amount_paid, Decimal('0'))


            # If full payment or overpayment, record in PaymentHistory
            PaymentHistory.objects.create(
                tenant=tenant,
                amount_paid=amount_paid,
                remaining_amount =remaining_amount,
                date_paid=timezone.now(),
                payment_method=payment_method,
                reference_id=reference_id,
                payment_screenshot=payment_screenshot,
                remarks='Full payment received',
                user=tenant.room.user
            )
            # Update tenant status as needed, for example, to mark no outstanding dues
            # tenant.partial_payment_made = True
            # tenant.save()

            # If the remaining amount is not equal to zero, also create a PaymentRemainder record
            if remaining_amount != Decimal('0'):
                PaymentRemainder.objects.create(
                    tenant=tenant,
                    amount_paid=amount_paid,
                    remaining_amount =  remaining_amount,
                    date_paid=timezone.now(),
                    payment_method=payment_method,
                    reference_id=reference_id,
                    payment_screenshot=payment_screenshot,
                    remarks='Manually added payment',
                    user=tenant.room.user  # Use tenant's associated user directly
                )
            tenant.partial_payment_made = True
            tenant.save()

            return redirect('Collections', property_id=selected_property.id)

            # You might record this in a different model or take other actions
            pass  # Replace with actual partial payment handling logic
        else:
            return HttpResponse("Invalid tenant ID provided.", status=400)
    else:
        return HttpResponse('Method not allowed', status=405)

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal

# Assuming your models.py file contains these:

from .models import AddProperty, Tenant, PaymentHistory, PaymentRemainder

def RemainderPage(request, property_id):
    try:
        selected_property = get_object_or_404(AddProperty, id=property_id)
        
        if request.method == 'POST':
            print("Received POST data:", request.POST)  # Debug print to console
            tenant_id = request.POST.get('tenantId')
            
            if tenant_id and tenant_id.isdigit():
                tenant = get_object_or_404(Tenant, id=int(tenant_id))
                payment_method = request.POST.get('payment_method', 'cash')
                reference_id = request.POST.get('reference_id', '') if payment_method == 'refId' else None
                payment_screenshot = request.FILES.get('payment_screenshot', None) if payment_method == 'screenshot' else None

                past_payments_sum = PaymentHistory.objects.filter(tenant=tenant).aggregate(Sum('amount_paid'))['amount_paid__sum'] or Decimal('0')
                new_payment = Decimal(request.POST.get('amount_paid_remainder', '0'))
                total_paid_to_date = past_payments_sum + new_payment
                total_due_for_period = tenant.total_due()
                new_remaining_amount = total_due_for_period - total_paid_to_date  

                # Record the payment
                PaymentHistory.objects.create(
                    tenant=tenant,
                    amount_paid=new_payment,
                    remaining_amount=max(new_remaining_amount, Decimal('0')),
                    date_paid=timezone.now(),
                    payment_method=payment_method,
                    reference_id=reference_id,
                    payment_screenshot=payment_screenshot,
                    remarks='Partial payment received' if new_remaining_amount > Decimal('0') else 'Full payment received',
                    user=tenant.room.user
                )

                # Update or clear remainder record
                if new_remaining_amount > Decimal('0'):
                    PaymentRemainder.objects.update_or_create(
                        tenant=tenant,
                        defaults={
                            'amount_paid': total_paid_to_date,
                            'remaining_amount': new_remaining_amount,
                            'date_paid': timezone.now(),
                            'payment_method': payment_method,
                            'reference_id': reference_id,
                            'payment_screenshot': payment_screenshot,
                            'remarks': 'Partial payment remaining',
                            'user': tenant.room.user
                        }
                    )
                    success_message = "Payment updated successfully. Remaining balance noted."
                else:
                    PaymentRemainder.objects.filter(tenant=tenant).delete()
                    success_message = "Full payment received and record cleared."
                
                messages.success(request, success_message)
                return redirect(f'/Collections/{property_id}/?section=remainder')
            else:
                return HttpResponse("Invalid tenant ID provided.", status=400)
        else:
            # Handle GET request to display the remainder payment form
            tenants_with_remainders = PaymentRemainder.objects.filter(tenant__room__property=selected_property)
            context = {
                'selected_property': selected_property,
                'tenants_with_remainders': tenants_with_remainders,
            }
            return render(request, 'payments/sections/remainder_page.html', context)
    except Exception as e:
        print("Error processing payment:", str(e))  # Print error to console
        return JsonResponse({'status': 'error', 'msg': str(e)}, status=500)





def Collections(request, property_id):
    selected_property = get_object_or_404(AddProperty, id=property_id)
    date_str = request.GET.get('date')
    section = request.GET.get('section', 'nameWithDues')
    user_properties = AddProperty.objects.filter(user=request.user)

    if date_str:
        filtered_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        tenants = Tenant.objects.filter(property=selected_property, due_date=filtered_date)
    else:
        today = timezone.now().date()
        tenants = Tenant.objects.filter(property=selected_property, due_date__lte=today, partial_payment_made=False)

    paymenthistory = PaymentHistory.objects.filter(tenant__property_id=property_id).order_by('-date_paid')

    remainders = PaymentRemainder.objects.filter(tenant__room__property=selected_property).annotate(
        latest_date=Max('date_paid')
    ).order_by('-date_paid')

    context = {
        'selected_property': selected_property,
        'tenants': tenants,
        'selected_date': date_str or today.strftime('%Y-%m-%d'),
        'paymenthistory': paymenthistory,
        'remainders': remainders,
        'user_properties': user_properties,
        'section': section,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('includes/partials/dues_table_partial.html', context, request=request)
        return HttpResponse(html)
    
    return render(request, 'payments/collections.html', context)



# views.py



# views.py
from django.core.mail import send_mail
from django.http import HttpResponse


from django.template import Context
from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    context = {
        'uid': 'dummy-uid',
        'token': 'dummy-token',
        'user': request.user,
        'site_name': 'Example Site',
        'protocol': 'http',
        'domain': 'example.com',
    }
    print(context)
    try:
        send_mail(
            'Test Subject',
            'This is a test message.',
            'muraliprasad996.996.mp@gmail.com',  # Ensure this matches DEFAULT_FROM_EMAIL
            ['muraliprasad142@gmail.com'],  # Replace with a valid recipient email
            fail_silently=False,
        )
        return HttpResponse('Test email sent.')
    except Exception as e:
        return HttpResponse(f'Error: {e}')

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import uuid
from .helpers import send_forget_password_mail
from .models import ChangedPassword

User = get_user_model()  # Get the user model

def ForgetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'No user found with this username')
            return redirect('forget_password')

        user = User.objects.get(username=username)
        token = str(uuid.uuid4())
        
        # Create or update the ChangedPassword with the token
        changed_password, created = ChangedPassword.objects.get_or_create(user=user)
        changed_password.forget_password_token = token
        changed_password.save()

        send_forget_password_mail(user.email, token)
        messages.success(request, 'An email has been sent.')
        return redirect('ForgetPassword')

    return render(request, 'registration/forget_password.html')

def ChangePassword(request, token):
    context = {}

    try:
        changed_password = ChangedPassword.objects.get(forget_password_token=token)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect(f'/change-password/{token}/')

            user = changed_password.user
            user.set_password(new_password)  # Properly hash the new password
            user.save()
            changed_password.forget_password_token = None  # Clear the token after successful reset
            changed_password.save()
            messages.success(request, 'Password has been changed successfully')
            return redirect('login_and_registration')

        context = {'token': token}
    except ChangedPassword.DoesNotExist:
        messages.error(request, 'Invalid or expired token')
        return redirect('ForgetPassword')

    return render(request, 'registration/change_password.html', context)
