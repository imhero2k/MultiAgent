# MultiAgent Route + Weather (PostGIS via Docker)

This project runs a multi-agent workflow that:
- gets a route from Google Maps,
- counts accidents near that route using PostGIS,
- fetches weather along the route.

## Stack

- Python
- AutoGen agents
- Google Maps APIs
- PostGIS (running in Docker)
- Open-Meteo API
- Ollama-compatible OpenAI endpoint (default: `http://localhost:11434/v1`)

## Prerequisites

- Python 3.10+
- Docker Desktop
- A Google Maps API key (`Directions` at minimum)
- Optional local Ollama model (default in code: `llama3.2`)

## 1) Start PostGIS in Docker

Run this container (matches defaults in `route_db_tools.py`):

```powershell
docker run --name postgis-multiagent `
  -e POSTGRES_DB=gisdb `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD="your_password_here" `
  -p 55432:5432 `
  -d postgis/postgis:16-3.4
```

If you already have a PostGIS container, just ensure:
- host: `localhost`
- port: `55432` (or update env vars below)
- database/user/password match your app env vars

## 2) Configure environment variables

Set these in your shell before running:

```powershell
$env:GOOGLE_MAPS_API_KEY="your_google_maps_key"
$env:OPENAI_API_KEY="ollama"
$env:OPENAI_BASE_URL="http://localhost:11434/v1"

$env:PGHOST="localhost"
$env:PGPORT="55432"
$env:PGDATABASE="gisdb"
$env:PGUSER="postgres"
$env:PGPASSWORD="your_password_here"
```

Notes:
- `OPENAI_API_KEY` is required by AutoGen even when using Ollama.
- If your PostGIS container uses different credentials/port, update the `PG*` variables.

## 3) Install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyautogen googlemaps tenacity polyline psycopg2-binary requests
```

## 4) Prepare PostGIS data/functions

Load your schema/data and required SQL function(s), including:
- crash points table (`vic_crash_nodes` expected by the code),
- function `accidents_along_route(encoded_polyline text, buffer_meters float)`.

You can run SQL with:

```powershell
docker exec -i postgis-multiagent psql -U postgres -d gisdb < routes.sql
```

If your SQL defines a different table/function name, update `route_db_tools.py` accordingly.

## 5) Run

```powershell
python main.py
```

The app writes the latest route polyline to `latest_polyline.txt`, then weather tools read it.

## Project files

- `main.py` - starts group chat with route + weather agents
- `route_agent.py` - registers route/PostGIS tools
- `route_tools.py` - Google Maps helper functions
- `route_db_tools.py` - PostGIS connection + accident counting helpers
- `weather_tools.py` - weather along route from Open-Meteo
- `weather_agent.py` - weather tool registration
