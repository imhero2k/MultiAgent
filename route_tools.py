# route_tools.py
import os
from typing import Any
import googlemaps
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import polyline as pl


def _gmaps() -> googlemaps.Client:
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_MAPS_API_KEY not set")
    return googlemaps.Client(key=key)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(Exception),
)
def directions(origin: str, destination: str, mode: str = "driving") -> dict[str, Any]:
    """Get driving directions using Google Maps Directions API."""
    g = _gmaps()
    res = g.directions(origin=origin, destination=destination, mode=mode)
    if not res:
        return {"error": "no route"}

    r = res[0]
    out: dict[str, Any] = {
        "summary": r.get("summary"),
        "overview_polyline": (r.get("overview_polyline") or {}).get("points"),
        "legs": [],
    }
    for leg in r.get("legs", []):
        out["legs"].append(
            {
                "distance": leg.get("distance", {}).get("text"),
                "duration": leg.get("duration", {}).get("text"),
                "start_address": leg.get("start_address"),
                "end_address": leg.get("end_address"),
            }
        )
    return out


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(Exception),
)
def distance_matrix(
    origins: list[str],
    destinations: list[str],
    mode: str = "driving",
) -> dict[str, Any]:
    """Get distance & duration between origins and destinations using Distance Matrix API."""
    g = _gmaps()
    dm = g.distance_matrix(origins=origins, destinations=destinations, mode=mode)
    # Return as plain dict (already JSON-serializable)
    return dm


def decode_polyline(encoded: str) -> list[dict[str, float]]:
    """Decode an encoded polyline into a list of {lat, lng} dicts."""
    coords = pl.decode(encoded)  # [(lat, lng), ...]
    return [{"lat": float(lat), "lng": float(lng)} for (lat, lng) in coords]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(Exception),
)
def roads_snap(points: list[dict[str, float]]) -> dict[str, Any]:
    """
    Snap a list of {lat, lng} to the road network using Roads API.

    Returns:
      {
        "snapped_polyline": str,
        "snapped_points": List[{lat: float, lng: float}]
      }
    """
    g = _gmaps()
    path = [(float(p["lat"]), float(p["lng"])) for p in points]
    res = g.snap_to_roads(path=path, interpolate=True)
    snapped = [
        {
            "lat": float(p["location"]["latitude"]),
            "lng": float(p["location"]["longitude"]),
        }
        for p in res
    ]
    encoded = pl.encode([(p["lat"], p["lng"]) for p in snapped])
    return {"snapped_polyline": encoded, "snapped_points": snapped}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(Exception),
)
def places_text(
    query: str,
    location: str | dict[str, float] | None = None,
    radius: int = 1500,
) -> dict[str, Any]:
    """
    Text search for places near a location.
    location can be "lat,lng" or dict {lat, lng} or None.
    """
    g = _gmaps()
    if isinstance(location, dict):
        loc = f'{location["lat"]},{location["lng"]}'
    else:
        loc = location
    res = g.places(query=query, location=loc, radius=radius)
    return res
