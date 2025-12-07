import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference

# Get all unique themes
all_conferences = Conference.objects.all()
print("All conferences and their themes:")
print("-" * 60)
for conf in all_conferences:
    print(f"Name: {conf.name}")
    print(f"Theme (raw): {conf.theme}")
    print(f"Theme (display): {conf.get_theme_display()}")
    print("-" * 60)
