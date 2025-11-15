# route_agent.py
from autogen.agentchat import ConversableAgent
import route_tools as rt
import route_db_tools as rdb  


class RouteAgentToolbox:
    """
    Registers routing tools to Autogen agents.
    - caller: the LLM agent that can *propose* tool calls (route_agent)
    - executor: the agent that actually *executes* the tools (user)
    """

    def register(self, caller: ConversableAgent, executor: ConversableAgent) -> None:
        # directions
        caller.register_for_llm(
            name="directions",
            description=(
                "Get driving directions using Google Maps Directions API. "
                "Args: origin (str), destination (str), mode (str, default 'driving'). "
                "Returns summary, legs, overview_polyline."
            ),
        )(rt.directions)
        executor.register_for_execution(name="directions")(rt.directions)

        # distance_matrix
        caller.register_for_llm(
            name="distance_matrix",
            description=(
                "Get distance & duration between origins and destinations using "
                "Google Distance Matrix API. Args: origins (list[str]), destinations (list[str]), "
                "mode (str, default 'driving')."
            ),
        )(rt.distance_matrix)
        executor.register_for_execution(name="distance_matrix")(rt.distance_matrix)

        # roads_snap
        caller.register_for_llm(
            name="roads_snap",
            description=(
                "Snap a list of {lat, lng} points to the road network using Roads API. "
                "Args: points (list[{lat: float, lng: float}]). "
                "Returns {snapped_polyline: str, snapped_points: list[{lat, lng}]}."
            ),
        )(rt.roads_snap)
        executor.register_for_execution(name="roads_snap")(rt.roads_snap)

        # decode_polyline
        caller.register_for_llm(
            name="decode_polyline",
            description="Decode an encoded polyline string into a list of {lat, lng} dicts.",
        )(rt.decode_polyline)
        executor.register_for_execution(name="decode_polyline")(rt.decode_polyline)

        # places_text
        caller.register_for_llm(
            name="places_text",
            description=(
                "Text search for places near a location using Places API. "
                "Args: query (str), location (str 'lat,lng' or {lat,lng}) or None, "
                "radius (int, meters). Returns raw Places API JSON."
            ),
        )(rt.places_text)
        executor.register_for_execution(name="places_text")(rt.places_text)

# accidents_along_route (keep if you want it as a standalone tool)
        caller.register_for_llm(
            name="accidents_along_route",
            description=(
                "Given an encoded polyline of a route and an optional buffer in meters, "
                "returns the number of crash points from vic_crash_nodes within that "
                "distance of the route in PostGIS."
            ),
        )(rdb.accidents_along_route)
        executor.register_for_execution(
            name="accidents_along_route"
        )(rdb.accidents_along_route
)
        caller.register_for_llm(
            name="route_with_accidents",
            description=(
                "Get fastest driving route between origin and destination and also "
                "count the number of accidents within a given buffer (meters) along "
                "the route using PostGIS. "
                "Args: origin (str), destination (str), "
                "mode (str, default 'driving'), buffer_meters (float, default 50). "
                "Returns: summary, legs, overview_polyline, buffer_meters, accident_count."
            ),
        )(rdb.route_with_accidents)
        executor.register_for_execution(
            name="route_with_accidents"
        )(rdb.route_with_accidents)
