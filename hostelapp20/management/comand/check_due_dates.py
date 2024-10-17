from django.core.management.base import BaseCommand
from django.utils import timezone
from hostelapp20.models import Hostel_details

class Command(BaseCommand):
    help = 'Check and display all students with due dates up to today'

    def handle(self, *args, **options):
        # Get the current date
        current_date = timezone.now().date()

        # Get students with due dates up to today
        students_with_due_dates = Hostel_details.objects.filter(due_date__lte=current_date)

        # Display the results
        self.stdout.write(self.style.SUCCESS('All students with due dates up to today:'))
        for student in students_with_due_dates:
            self.stdout.write(f'- ID: {student.id}, Name: {student.guest_name}, Due Date: {student.due_date}')
