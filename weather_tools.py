import requests
import polyline
from typing import Any, List, Dict

def get_current_weather(lat: float, lng: float) -> Dict[str, Any]:
    """
    Get current weather for a specific location using Open-Meteo API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current_weather": "true"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("current_weather", {})
    except Exception as e:
        return {"error": str(e)}

def get_weather_along_route(encoded_polyline: str):
    """
    Decodes the polyline, samples points (start, middle, end),
    and fetches current weather for each point.
    """
    points = polyline.decode(encoded_polyline)
    if not points:
        return "Could not decode polyline."

    # Sample 3 points: start, middle, end
    sampled_points = [
        points[0],
        points[len(points) // 2],
        points[-1]
    ]

    results = []
    for i, (lat, lng) in enumerate(sampled_points):
        label = "Start" if i == 0 else ("End" if i == 2 else "Middle")
        weather = get_current_weather(lat, lng)
        results.append(f"{label} ({lat:.4f}, {lng:.4f}): {weather}")

    return "\n".join(results)


def get_weather_for_last_route():
    """
    Fetches weather for the last calculated route by reading 'latest_polyline.txt'.
    """
    try:
        with open("latest_polyline.txt", "r") as f:
            encoded_polyline = f.read().strip()
        if not encoded_polyline:
            return "No route found in cache."
        return get_weather_along_route(encoded_polyline)
    except FileNotFoundError:
        return "No route has been calculated yet."
    except Exception as e:
        return f"Error reading route cache: {e}"
