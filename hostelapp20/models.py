from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, date
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
    

    def save(self, *args, **kwargs):
        # Update the total rooms count when a room is added or updated
        if not self.pk:
            self.property.total_rooms = Room.objects.filter(property=self.property).count() + 1
        super().save(*args, **kwargs)
        self.update_property_statistics()

    def delete(self, *args, **kwargs):
        property_instance = self.property
        super(Room, self).delete(*args, **kwargs)
        property_instance.total_rooms = Room.objects.filter(property=property_instance).count()
        property_instance.save()
        self.update_property_statistics()

    def update_property_statistics(self):
        # Calculate total occupied beds and free beds
        total_beds = Room.objects.filter(property=self.property).aggregate(Sum('number_of_share'))['number_of_share__sum']
        occupied_beds = Tenant.objects.filter(property=self.property).count()
        free_beds = total_beds - occupied_beds if total_beds else 0

        # Update the property with the new statistics
        self.property.occupied_beds = occupied_beds
        self.property.free_beds = free_beds
        self.property.save()

        

def upload_to_govt_id_front(instance, filename):
    base, extension = os.path.splitext(filename)
    filename = slugify(base) + extension
    return os.path.join('proof', 'govt_id_front', filename)

def upload_to_govt_id_back(instance, filename):
    base, extension = os.path.splitext(filename)
    filename = slugify(base) + extension
    return os.path.join('proof', 'govt_id_back', filename)


from datetime import datetime, date

class Tenant(models.Model):
    # your existing fields
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
    next_due_date = models.DateField(null=True, blank=True)
    allocated_bed = models.CharField(max_length=100, null=True)
    rent = models.CharField(max_length=100, null=True)
    advance = models.CharField(max_length=10, null=True, blank=True)
    tenant_image = models.ImageField(upload_to='tenant_images/', null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    property = models.ForeignKey(AddProperty, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Unnamed Tenant"
        
        
    def save(self, *args, **kwargs):
        # Check if joining date has changed and update due date accordingly
        if self.pk:
            old_instance = Tenant.objects.get(pk=self.pk)
            if old_instance.joining_date != self.joining_date:
                self.next_due_date = self.calculate_next_due_date()
        else:
            self.next_due_date = self.calculate_next_due_date()

        # Save the tenant data first
        super().save(*args, **kwargs)

        # Update the occupancy statistics for the room and property
        self.room.update_property_statistics()

    def delete(self, *args, **kwargs):
        # Delete the tenant data first
        super().delete(*args, **kwargs)

        # Update the occupancy statistics for the room and property after deletion
        self.room.update_property_statistics()

    def calculate_next_due_date(self):
        if not self.joining_date:
            return None
        if isinstance(self.joining_date, str):
            self.joining_date = datetime.strptime(self.joining_date, '%Y-%m-%d').date()

        today = date.today()
        due_date = self.joining_date.replace(year=today.year, month=today.month)

        if due_date < today:
            if today.month == 12:
                due_date = due_date.replace(year=today.year + 1, month=1)
            else:
                due_date = due_date.replace(month=today.month + 1)
        
        return due_date



class Remainder(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    payment_type = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('online', 'Online'), ('screenshot', 'Screenshot')])
    reference_number = models.CharField(max_length=12, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)

    def __str__(self):
        return f'Remainder for {self.tenant.name} on {self.payment_date}'
    
    

class History(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('screenshot', 'Screenshot'),
        ('online', 'Online Payment')
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    time_paid = models.TimeField(auto_now_add=True)  # Ensure this line is included
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', blank=True, null=True)
    payment_reference = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.amount_paid}"



class ChangedPassword(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username