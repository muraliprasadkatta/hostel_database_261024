from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
import os
from django.utils.text import slugify



# Now you can use timezone.now() to get the current date and time in a time zone-aware format:
current_time = timezone.now()


def normalize_mobile_number(mobile):
    if mobile.startswith('+91'):
        mobile = mobile[3:]
    return mobile.strip()

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=120)
    is_registered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Normalize mobile number
        if self.mobile_number:
            self.mobile_number = normalize_mobile_number(self.mobile_number)
        # Set is_registered to True when saving the user for the first time
        if not self.pk:
            self.is_registered = True
        super().save(*args, **kwargs)

# for add hostel data form

class AddProperty(models.Model):
    hostelname = models.CharField(max_length=100)
    ownername = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    address = models.CharField(max_length=1000)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    total_rooms = models.IntegerField(default=0)
    occupied_beds = models.IntegerField(default=0)
    free_beds = models.IntegerField(default=0)



    def __str__(self):
        return f"{self.hostelname} - {self.ownername}"


from django.db import models
from django.conf import settings

class ManagementPin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pin = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Management PIN for {self.user.username}"



class Room(models.Model):
    room_number = models.IntegerField() 
    floor_type = models.CharField(max_length=50)
    number_of_share = models.PositiveIntegerField()
    available_room_or_not = models.CharField(max_length=30)
    remarks = models.CharField(max_length=500, null=True )
    room_facilities = models.TextField(max_length=1000, null=True)
    property = models.ForeignKey('AddProperty', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room_number} - {self.property.hostelname}"
    


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, [31,
        29 if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


def upload_to_govt_id_front(instance, filename):
    base, extension = os.path.splitext(filename)
    filename = slugify(base) + extension
    return os.path.join('proof', 'govt_id_front', filename)

def upload_to_govt_id_back(instance, filename):
    base, extension = os.path.splitext(filename)
    filename = slugify(base) + extension
    return os.path.join('proof', 'govt_id_back', filename)

class Tenant(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=10, null=True)
    adhar_number = models.CharField(max_length=12, null=True)
    govt_id_front = models.ImageField(upload_to=upload_to_govt_id_front, null=True)
    govt_id_back = models.ImageField(upload_to=upload_to_govt_id_back, null=True)
    state = models.CharField(max_length=100, null=True)
    dist = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=6, null=True)
    city = models.CharField(max_length=100, null=True)
    door_no = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    bike_number = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(null=True)
    due_date = models.DateField()
    allocated_bed = models.CharField(max_length=100, null=True)
    rent = models.CharField(max_length=100, null=True)
    advance = models.CharField(max_length=10, null=True, blank=True)
    tenant_image = models.ImageField(upload_to='tenant_images/', null=True)
    dues_cleared = models.BooleanField(default=False)
    partial_payment_made = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    property = models.ForeignKey(AddProperty, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def total_due(self):
        """
        Calculates the total due amount for the tenant.
        This is a simplistic example that assumes the total due is the rent
        minus any advance payment made.
        You should adjust this calculation based on your application's requirements.
        """
        try:
            rent_amount = Decimal(self.rent) if self.rent and self.rent.strip().replace(',', '').isdigit() else Decimal('0')
        except (ValueError, decimal.InvalidOperation):
            rent_amount = Decimal('0')
            
        try:
            advance_paid = Decimal(self.advance) if self.advance and self.advance.strip().replace(',', '').isdigit() else Decimal('0')
        except (ValueError, decimal.InvalidOperation):
            advance_paid = Decimal('0')

        # Assuming the total due is rent minus advance. Adjust as needed.
        total_due_amount = rent_amount - advance_paid
        return total_due_amount



    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Unnamed Tenant"


    def save(self, *args, **kwargs):
        # Ensure joining_date is a date object
        if isinstance(self.joining_date, str):
            self.joining_date = datetime.strptime(self.joining_date, '%Y-%m-%d').date()
        
        # Set a default for due_date if it's not set
        if not self.due_date:
            self.due_date = self.joining_date

        # Ensure due_date is a date object
        if isinstance(self.due_date, str):
            self.due_date = datetime.strptime(self.due_date, '%Y-%m-%d').date()
        
        current_date = timezone.now().date()

        # If the due_date is before today, update it
        if self.due_date < current_date:
            # Update the due_date to the next month on the same day as joining_date
            while self.due_date < current_date:
                self.due_date += relativedelta(months=+1)
        # Note: The loop condition is changed to '<' instead of '<='
        # This ensures that if due_date == current_date, it doesn't increment

        super().save(*args, **kwargs)



class PaymentHistory(models.Model):
    amount_paid = models.IntegerField()
    remaining_amount =models.CharField(max_length=10, blank=True, null=True)
    date_paid = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=100) # Stores 'Cash', 'Payment Reference ID', 'Payment Screenshot'
    reference_id = models.CharField(max_length=100, blank=True, null=True) # For 'Payment Reference ID'
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True) # For 'Payment Screenshot'
    remarks = models.TextField(blank=True, null=True)
    tenant = models.ForeignKey(Tenant, related_name='payments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.tenant.name} on {self.date_paid}"

    # In PaymentHistory model
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method first
        self.update_tenant_due_date()

    def update_tenant_due_date(self):
        # Ensure we aggregate payments correctly and consider only payments up to the current due date
        total_paid = PaymentHistory.objects.filter(
            tenant=self.tenant, 
            date_paid__lte=self.tenant.due_date
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        
        # Assuming `rent` is stored as a string that represents an integer
        try:
            rent = int(self.tenant.rent)
        except ValueError:
            # Log or handle tenants with invalid rent values
            return

        if total_paid >= rent:
            # Update the due_date to the next month if the rent is fully paid
            next_due_date = monthdelta(self.tenant.due_date, 1)
            self.tenant.due_date = next_due_date
            self.tenant.dues_cleared = True  # Optionally mark dues as cleared
            self.tenant.save()



class PaymentRemainder(models.Model):
    amount_paid = models.IntegerField()
    remaining_amount =models.CharField(max_length=10, blank=True, null=True)
    date_paid = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=100) # Stores 'Cash', 'Payment Reference ID', 'Payment Screenshot'
    reference_id = models.CharField(max_length=100, blank=True, null=True) # For 'Payment Reference ID'
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True) # For 'Payment Screenshot'
    remarks = models.TextField(blank=True, null=True)
    tenant = models.ForeignKey(Tenant, related_name='remainders', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.amount_paid} by {self.tenant.name} "


class ChangedPassword(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username