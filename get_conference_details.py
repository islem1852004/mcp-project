import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference

try:
    conf = Conference.objects.get(name__icontains="user")
    print("Conference Details:")
    print("-" * 60)
    print(f"Name: {conf.name}")
    print(f"Theme: {conf.get_theme_display()}")
    print(f"Location: {conf.location}")
    print(f"Dates: {conf.start_date} to {conf.end_date}")
    print(f"Description: {conf.description}")
    print("-" * 60)
except Conference.DoesNotExist:
    print("Conference 'user' not found.")
except Conference.MultipleObjectsReturned:
    print("Multiple conferences found matching 'user'.")
