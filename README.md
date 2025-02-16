# OOYE - Hostel Management System

OOYE is a hostel management system designed to manage tenants, properties, and payments efficiently.

---

## **Features**
- Tenant Management
- Property Switching
- Rent and Payment Tracking
- Bed and Room Allocation

---

## **Installation Guide**

### Prerequisites
- Python 3.8 or later
- Pip package manager

### Setup Instructions
1. Clone or download the repository:
   ```bash
   git clone https://github.com/muraliprasadkatta/hostel_database_261024.git
   cd your-repo-name




------------------------------------------------------------------

Project Overview
Project Name: OOYE Tenant Management System
Frameworks/Technologies:
Backend: Django, Python
Frontend: HTML, CSS, JavaScript, AJAX
Database: PostgreSQL (both local and Heroku production)
Deployment Platform: Heroku
Domain Provider: GoDaddy (ooye.in)
Static & Media Files Storage: Cloudinary (for production)
Email Provider: GoDaddy Secure Server (SMTP)
OAuth Integration: Google OAuth2 (for user login)


---------------------------------------------------------------------


Project Structure
Models:

AddProperty (for property details)
Room (for room data)
Tenant (for tenant details and payments)
Views:

DisplayRooms: View to display rooms under a property.
TenantDetails: View to fetch tenant details based on property, room, and tenant IDs.
search_suggestions: AJAX-based search for tenants using property ID.
Templates:

base.html: The main layout for the dashboard and other pages.
data/display_rooms.html: Displays rooms and bed statistics for a property.
registration/forgot_password_modal.html: Handles password reset functionality.
Forms and Modals:

Add/Edit Room Modal
Payment Forms (dues, initial payment)


-------------------------------------------------------------------

Key Commands & Configurations
Heroku Setup:


# Add Heroku remote
heroku git:remote -a <heroku-app-name>

# Set environment variables on Heroku
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set DATABASE_URL=<heroku-database-url>

# Disable static file collection for troubleshooting
heroku config:set DISABLE_COLLECTSTATIC=1

# Push code to Heroku
git push heroku main


-----------------------------------------------------
Local Database Configuration (.env file):

DB_NAME=hostel_database_261024
DB_USER=murali
DB_PASSWORD=Hosteldb2024
DB_HOST=localhost
DB_PORT=5432
DEBUG=True


Static and Media Files Setup:

Local: Use MEDIA_ROOT and STATIC_ROOT.
Production: Use Cloudinary (cloudinary_storage).



------------------------------------------------------------

DNS Configuration
Domain Name: ooye.in
CNAME: Configured for Heroku (transparent-sheep-xxxxxx.herokuapp.com)
Forwarding:
Forward ooye.in to https://www.ooye.in.


------------------------------------------------------------

Common Issues and Solutions
Server Error on Dashboard:

Cause: Missing static/media files or database mismatch.
Solution: Ensure static files are collected and database migrations are applied.
Search Suggestions Not Redirecting:

Cause: Incorrect URL format for tenant details.
Solution: Modify JavaScript to include the correct room number dynamically.


-----------------------------------------------------------------------


Developer Notes
Environment Variables: Use .env files to manage sensitive configurations.
Static Files: Run python manage.py collectstatic before deploying to production.
Database Migration: Run python manage.py migrate after making model changes.
Authentication: OAuth-based login is integrated using Google OAuth2.


------------------------------------------------------------

how to connect the google oauth

Step 1: Install the Required Package

Install social-auth-app-django, which integrates OAuth2 with Django authentication.

pip install social-auth-app-django


Update requirements.txt to include:

social-auth-app-django

Step 2: Add Required Settings in settings.py

# Add 'social_django' to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'social_django',
]

# Add authentication backends
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',  # Default Django auth backend
)

# Add the context processor for social auth in TEMPLATES
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Google OAuth2 settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<YOUR_GOOGLE_CLIENT_ID>'  # Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<YOUR_GOOGLE_CLIENT_SECRET>'  # Client Secret

# Redirect URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'  # Redirect after login
LOGOUT_REDIRECT_URL = 'login'  # Redirect after logout

# Security and session management
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'  # Error handling on login failure
SOCIAL_AUTH_RAISE_EXCEPTIONS = False  # Avoid raising exceptions in production


Step 3: Set Up URLs

Add the authentication URLs in urls.py.

from django.urls import path, include

urlpatterns = [
    ...
    path('auth/', include('social_django.urls', namespace='social')),
]


Step 4: Create Google OAuth Credentials
Go to Google Cloud Console.
Create a new project or select an existing one.
Navigate to "APIs & Services" > "Credentials".
Click "Create Credentials" > "OAuth Client ID".
Application Type: Web Application

Authorized redirect URIs:
https://<your-domain>/auth/complete/google/


Example for local development:
http://127.0.0.1:8000/auth/complete/google/

Copy the Client ID and Client Secret to the settings.py.

Step 5: Update Database and Create Migrations
Run the following commands:

python manage.py migrate


Step 6: Add Login Link in Templates
You can add a login button or link in your HTML:

<a href="{% url 'social:begin' 'google-oauth2' %}">Login with Google</a>


Step 7: Testing and Debugging
Visit the login URL to test authentication:
http://127.0.0.1:8000/auth/login/google-oauth2/


Once authenticated, you should be redirected to the dashboard or the page specified in LOGIN_REDIRECT_URL.

If any issues arise, check logs or debug with:

import logging
logger = logging.getLogger('social')
logger.setLevel(logging.DEBUG)


Step 8: Configure Environment Variables (for Heroku)
Set the Google OAuth credentials on Heroku:

heroku config:set SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<your-google-client-id>
heroku config:set SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=<your-google-client-secret>


Current Google Cloud Project Details
Project Name: Hostel data
Project ID: hostel-data-420508
Project Number: 673649864075



----------------------------------------------------------

Data base manual creat row why and how 

Manual Database Row Creation - Explanation
Why did we create the row manually?
We manually added a row to the database to test the search functionality of our application. This was done to verify if the data stored in the database appears in the search results when queried through the frontend search bar. Sometimes, during development, real-time data may not be available or fully set up, so we create dummy data manually to perform validation.


-----------------------------------------------------------

for getting image from server use the cloundary 

### Cloudinary Integration Notes

1. **Why Cloudinary?**
   - Scalable image storage and delivery.
   - Faster page load times with CDN.
   - Automatic image optimization and transformations.

2. **Steps for Integration:**

   **a. Create Account & Get Credentials**  
   - Sign up at [cloudinary.com](https://cloudinary.com).  
   - Copy Cloud Name, API Key, and API Secret from the dashboard.

   **b. Install Cloudinary Library**  
   - Run the command:  
     ```bash
     pip install django-cloudinary-storage
     ```

   **c. Configure Settings**  
   - Add the following to `settings.py`:
     ```python
     import environ

     env = environ.Env()
     environ.Env.read_env()

     CLOUDINARY_STORAGE = {
         'CLOUD_NAME': env('CLOUD_NAME'),
         'API_KEY': env('CLOUDINARY_API_KEY'),
         'API_SECRET': env('CLOUDINARY_API_SECRET'),
         'folder': 'property_images'
     }

     DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
     ```

   **d. Add Credentials to `.env` File**  
     ```
     CLOUD_NAME=your_cloud_name
     CLOUDINARY_API_KEY=your_api_key
     CLOUDINARY_API_SECRET=your_api_secret
     ```

   **e. Update Model**  
   - Use `ImageField` in your models. Example:
     ```python
     class Property(models.Model):
         name = models.CharField(max_length=255)
         image = models.ImageField(upload_to='property_images/', null=True, blank=True)
     ```

   **f. Use in Templates**  
   - Display images with:  
     ```html
     <img src="{{ property.image.url }}" alt="{{ property.name }}">
     ```

3. **Tips:**
   - **Testing:** Images uploaded locally will also go to Cloudinary if correctly configured.
   - **Heroku:** Disable static collection during deployment if needed:  
     ```bash
     heroku config:set DISABLE_COLLECTSTATIC=1
     ```



----------------------------------------------------------------------------------
connection for collection and dues and remainder

README: Handling Dues and Remainder Sections in the Django Application

This document provides a clear overview of how the dues_view function and the associated template logic work to display the Dues and Remainder sections in the application.


1️⃣ Overview

The dues_view handles both Dues and Remainders for a selected property. The collections/sections/dues.html template includes two sections that users can toggle between using buttons.

2️⃣ Key Components

🛠️ View Function: dues_view

def dues_view(request, property_id):
    selected_property = None
    user_properties = AddProperty.objects.filter(user=request.user)

    # Process image URLs for sidebar properties & find selected property
    for property in user_properties:
        if property.image:
            property.image_url = property.image.url.replace("/http%3A/", "http://")
        else:
            property.image_url = None

        # Identify selected property directly from this loop
        if property.id == property_id:
            selected_property = property

    if selected_property is None:
        raise Http404("Selected property not found")

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

    # Fetch remainder records
    remainders = Remainder.objects.filter(tenant__property=selected_property)

    context = {
        'selected_property': selected_property,
        'tenants_with_due_today': tenants_with_due_today,
        'selected_date': selected_date,
        'date_filtered': date_filtered,
        'user_properties': user_properties,
        'remainders': remainders,
    }

    # 🔍 **AJAX Request Handling**
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'collections/sections/partials/dues_body.html', context)

    return render(request, 'collections/sections/dues.html', context)



    
** Explanation:**
Property Identification: Loops through properties to identify the selected property.

Dues Filtering: Filters tenants based on the due date and property.

Remainders Query: Fetches remainder records linked to the selected property.

AJAX Support: If the request is AJAX, it only returns the partial content.



3️⃣ Template Structure

📄 **Main Template: **collections/sections/dues.html



<div class="paymentContainer">
    <div class="button-container">
        <!-- Toggle Buttons -->
        <button id="duesBtn" onclick="showSection('dues')">Dues</button>
        <button id="remainderBtn" onclick="showSection('remainder')">Remainder</button>
    </div>

    <!-- Dynamic Content Sections -->
    <div id="duesContent" style="display: block;">
        {% include 'collections/sections/partials/dues_body.html' %}
    </div>

    <div id="remainderContent" style="display: none;">
        {% include 'collections/sections/partials/remainder_body.html' %}
    </div>
</div>

<script>
// Function to toggle between Dues and Remainder sections
function showSection(section) {
    const dues = document.getElementById('duesContent');
    const remainder = document.getElementById('remainderContent');

    if (section === 'dues') {
        dues.style.display = 'block';
        remainder.style.display = 'none';
    } else if (section === 'remainder') {
        dues.style.display = 'none';
        remainder.style.display = 'block';
    } else {
        console.error('Invalid section name:', section);
    }
}
</script>

🔍 Explanation:

Two buttons allow users to toggle between the Dues and Remainder sections.

The content for both sections is included using Django's {% include %} tag.

JavaScript handles the visibility of each section dynamically.

5️⃣ Troubleshooting Tips

🛑 No Remainder Records Displayed?

Check database records: Remainder.objects.all().

Confirm tenants exist for the selected property.

🔄 AJAX Content Not Updating?

Inspect network tab in DevTools to monitor AJAX requests.

⚠️ Section Toggle Not Working?

Confirm button IDs and JavaScript logic.


-----------------------------------------------------------------------------