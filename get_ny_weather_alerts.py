import asyncio
import httpx
from typing import Any

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """
    Make a request to the NWS API with proper error handling.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=40.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request: {e}")
            return None

def format_alert(feature: dict) -> str:
    """
    Format an alert feature into a readable string.
    """
    props = feature["properties"]
    
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a US state.
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    
    return "\n========================\n".join(alerts)

async def main():
    print("Fetching weather alerts for New York (NY)...")
    print("=" * 50)
    alerts = await get_alerts("NY")
    print(alerts)

if __name__ == "__main__":
    asyncio.run(main()) 