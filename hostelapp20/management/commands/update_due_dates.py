from django.core.management.base import BaseCommand
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from hostelapp20.models import Tenant, PaymentHistory, Remainder  # Replace 'myapp' with your actual app name

class Command(BaseCommand):
    help = 'Updates due dates for tenants based on payments and current date.'

    def handle(self, *args, **options):
        tenants = Tenant.objects.filter(due_date__lt=timezone.now())
        for tenant in tenants:
            payments_sum = tenant.payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            remainder_sum = tenant.remainders.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
            
            total_paid = payments_sum + remainder_sum
            
            try:
                rent_amount = float(tenant.rent)
            except ValueError:
                self.stdout.write(self.style.WARNING(f'Skipped tenant {tenant.id} due to invalid rent value.'))
                continue
            
            if total_paid >= rent_amount:
                if not tenant.dues_cleared:
                    tenant.due_date += relativedelta(months=+1)  # Update only on full payment
                    tenant.dues_cleared = True
                    tenant.partial_payment_made = False  # Reset flag as dues are cleared
                    tenant.save()
                    self.stdout.write(self.style.SUCCESS(f'Full payment received, updated due date for tenant {tenant.name}.'))
            else:
                tenant.partial_payment_made = True  # Mark that a partial payment was made
                tenant.save()
                self.stdout.write(self.style.NOTICE(f'Partial payment recorded for tenant {tenant.name}, no due date change.'))
