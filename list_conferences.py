import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference

conferences = Conference.objects.all()

if not conferences.exists():
    print("No conferences found.")
else:
    print("Available Conferences:")
    print("-" * 60)
    for conf in conferences:
        print(f"Name: {conf.name}")
        print(f"Dates: {conf.start_date} to {conf.end_date}")
        print(f"Location: {conf.location}")
        print(f"Theme: {conf.get_theme_display()}")
        print(f"Description: {conf.description}")
        print("-" * 60)
