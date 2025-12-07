import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference

# Filter by theme code
theme_filter = "CS&IA"
conferences = Conference.objects.filter(theme=theme_filter)

print(f"Conferences filtered by theme: '{theme_filter}' (Informatique et IA)")
print("-" * 60)

if not conferences.exists():
    print(f"No conferences found for theme '{theme}'.")
else:
    for conf in conferences:
        print(f"Name: {conf.name}")
        print(f"Dates: {conf.start_date} to {conf.end_date}")
        print(f"Location: {conf.location}")
        print(f"Theme: {conf.get_theme_display()}")
        print("-" * 60)
