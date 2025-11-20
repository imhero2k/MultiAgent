# route_db_tools.py
import os
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

import route_tools as rt  # 👈 so we can call directions()


def _pg_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "55432")),   # host port -> container 5432
        dbname=os.getenv("PGDATABASE", "gisdb"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "FIT5137@Monash"),
    )


def accidents_along_route(
    encoded_polyline: str,
    buffer_meters: float = 50.0,
) -> dict[str, Any]:
    conn = _pg_conn()
    try:
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT accidents_along_route(%s, %s) AS count",
                (encoded_polyline, buffer_meters),
            )
            row = cur.fetchone()
            count = row["count"] if row is not None else 0
    finally:
        conn.close()

    return {
        "encoded_polyline": encoded_polyline,
        "buffer_meters": buffer_meters,
        "accident_count": int(count),
    }


def route_with_accidents(
    origin: str,
    destination: str,
    mode: str = "driving",
    buffer_meters: float = 50.0,
) -> dict[str, Any]:
    """
    High-level helper:
      1) Get fastest route with directions()
      2) Use overview_polyline to count accidents_along_route()
    Returns summary, legs, overview_polyline, buffer_meters, accident_count.
    """
    # 1) Directions from Google Maps
    base = rt.directions(origin=origin, destination=destination, mode=mode)

    poly = base.get("overview_polyline")
    if not poly:
        # no route? still return something sensible
        return {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "summary": base.get("summary"),
            "legs": base.get("legs", []),
            "overview_polyline": poly,
            "buffer_meters": buffer_meters,
            "accident_count": None,
        }

    # 2) Count accidents along that polyline
    acc = accidents_along_route(poly, buffer_meters=buffer_meters)

    # Cache the polyline for other agents (e.g. weather_agent)
    try:
        with open("latest_polyline.txt", "w") as f:
            f.write(poly)
    except Exception as e:
        print(f"Warning: Could not cache polyline: {e}")

    return {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "summary": base.get("summary"),
        "legs": base.get("legs", []),
        "overview_polyline": poly,
        "buffer_meters": buffer_meters,
        "accident_count": acc["accident_count"],
    }
