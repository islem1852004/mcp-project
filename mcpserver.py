import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConferance.settings')
import django
django.setup()

from ConferenceAPP.models import Conference  # Adaptez vos apps/modèles
from SessionApp.models import Session
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

mcp = FastMCP("Conference Assistant")

@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    def get_confs():
        return list(Conference.objects.all())
    confs = await sync_to_async(get_confs)()
    if not confs: return "No conferences found."
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in confs])

@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    def get_conf():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    conf = await sync_to_async(get_conf)()
    if conf == "MULTIPLE": return "Multiple conferences found."
    if not conf: return f"Conference '{name}' not found."
    return f"Name: {conf.name}\nTheme: {conf.get_theme_display()}\nLocation: {conf.location}\nDates: {conf.start_date} to {conf.end_date}\nDescription: {conf.description}"

@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    def get_sess():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()), conf
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    result, conf = await sync_to_async(get_sess)()
    if result == "MULTIPLE": return "Multiple conferences found."
    if conf is None: return f"Conference '{conference_name}' not found."
    if not result: return f"No sessions for '{conf.name}'."
    return "\n".join([f"- {s.title} ({s.start_time}-{s.end_time}) in {s.room}\n  Topic: {s.topic}" for s in result])

@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme."""
    def get_filtered():
        return list(Conference.objects.filter(theme__icontains=theme))
    confs = await sync_to_async(get_filtered)()
    if not confs: return f"No conferences for theme '{theme}'."
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in confs])

if __name__ == "__main__":
    mcp.run(transport="stdio")
