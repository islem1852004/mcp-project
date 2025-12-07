import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference

try:
    conf = Conference.objects.get(name__icontains="user")
    sessions = conf.sessions.all()
    
    print(f"Sessions for Conference: {conf.name}")
    print("-" * 60)
    
    if not sessions.exists():
        print(f"No sessions found for '{conf.name}'.")
    else:
        for session in sessions:
            print(f"Title: {session.title}")
            print(f"Time: {session.start_time} - {session.end_time}")
            print(f"Room: {session.room}")
            print(f"Topic: {session.topic}")
            print("-" * 60)
            
except Conference.DoesNotExist:
    print("Conference 'user' not found.")
except Conference.MultipleObjectsReturned:
    print("Multiple conferences found matching 'user'.")
