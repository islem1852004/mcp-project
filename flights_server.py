from mcp.server.fastmcp import FastMCP
import os
import json
mcp=FastMCP(name='FlightsServer')
FLIGHTS_PATH = os.path.join(os.path.dirname(__file__), "flights.json")
def _load_flights():
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])
@mcp.resource("flights://today")
def flights_resource():
    """
    Resource qui expose la liste des vols du jour.
    L'URL 'flights://today' sera visible par Copilot/Claude.
    """
    with open(FLIGHTS_PATH, "r", encoding="utf-8") as f:
        return f.read()
@mcp.tool()
# outil pour rechercher un vol par son numéro
def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""
 
    flights = _load_flights()
 
    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return f"""
                 Vol {flight["flight_number"]} ({flight["airline"]})
            {flight["departure_city"]} → {flight["arrival_city"]}
            Départ : {flight["departure_time"]} | Arrivée : {flight["arrival_time"]}
            Statut : {flight["status"]}
            """
    return f"Vol {flight_number} non trouvé aujourd'hui."
# 2.b - Filtrage générique par critère (ex: destination, compagnie, etc.)

@mcp.tool()
def filter_flights(field: str, value: str) -> str:
    """
    Filtre les vols selon un champ et une valeur.
    Exemples de field : destination, airline, departure_city, status, gate...
    """
    allowed_fields = ["destination", "airline", "departure_city", "arrival_city", 
                      "status", "gate", "terminal", "aircraft_type"]
    
    if field not in allowed_fields:
        return f"Champ '{field}' non autorisé. Champs possibles : {', '.join(allowed_fields)}"

    flights = _load_flights()
    matches = [f for f in flights if str(f.get(field, "")).lower() == value.lower()]

    if not matches:
        return f"Aucun vol trouvé avec {field} = {value}"

    result = f"{len(matches)} vol(s) trouvé(s) pour {field} = {value}:\n\n"
    for f in matches:
        delay = f" (retard {f.get('delay_minutes', 0)} min)" if f.get('delay_minutes', 0) > 0 else ""
        result += f"• {f['flight_number']} {f['departure_city']} → {f['arrival_city']} | {f['departure_time']} | Statut: {f['status']}{delay}\n"
    
    return result.strip()


# 2.c - TOOL DEMANDÉ : Vols ayant un statut particulier

@mcp.tool()
def get_flights_by_status(status: str) -> str:
    """
    Retourne tous les vols ayant un statut précis.
    Statuts possibles dans les données : "À l'heure", "Retardé", "Annulé", "Embarquement", "En vol", etc.
    """
    valid_statuses = {"à l'heure", "retardé", "annulé", "embarquement", "en vol", "décollé", "atterri"}
    status_norm = status.strip().lower()

    if status_norm not in valid_statuses:
        return f"Statut '{status}' non reconnu. Utilisez un des statuts suivants : {', '.join(sorted(valid_statuses))}"

    flights = _load_flights()
    matches = [f for f in flights if f.get("status", "").lower() == status_norm]

    if not matches:
        return f"Aucun vol avec le statut « {status} » aujourd'hui."

    result = f"{len(matches)} vol(s) avec le statut « {status} » :\n\n"
    for f in matches:
        delay_info = f" – Retard : {f.get('delay_minutes', 0)} min" if f.get('delay_minutes') else ""
        result += f"• {f['flight_number']} | {f['departure_city']} → {f['arrival_city']} | Départ prévu : {f['departure_time']}{delay_info}\n"

    return result.strip()

# 2.d - TOOL LIBRE (logique métier pertinente que j’ai choisie)

@mcp.tool()
def get_next_departures(from_city: str, limit: int = 5) -> str:
    """
    Donne les prochains vols au départ d'une ville donnée, triés par heure de départ.
    Très utile pour un passager qui arrive à l'aéroport et veut savoir quoi voir ensuite.
    """
    if limit < 1 or limit > 20:
        return "Le paramètre limit doit être entre 1 et 20."

    flights = _load_flights()
    
    # Filtre + tri par heure de départ
    upcoming = [
        f for f in flights 
        if f.get("departure_city", "").lower() == from_city.lower()
    ]
    upcoming.sort(key=lambda x: x.get("departure_time", "99:99"))

    if not upcoming:
        return f"Aucun vol au départ de {from_city.title()} aujourd'hui."

    result = f"Prochains départs depuis {from_city.title()} (max {limit}):\n\n"
    for f in upcoming[:limit]:
        status_icon = "⚠️" if f['status'].lower() == "retardé" else "✅"
        delay = f" (+{f.get('delay_minutes', 0)} min)" if f.get('delay_minutes', 0) > 0 else ""
        result += f"{status_icon} {f['flight_number']} → {f['arrival_city']} | {f['departure_time']}{delay} | Porte {f.get('gate', '–')}\n"

    return result.strip()
#pour lancer le serveur de vols 
if __name__ == "__main__":
    mcp.run(transport="stdio")
