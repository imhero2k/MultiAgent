import os
from autogen.agentchat import ConversableAgent, GroupChat, GroupChatManager

from route_agent import RouteAgentToolbox
from weather_agent import WeatherAgentToolbox

if __name__ == "__main__":
    # We still need Google Maps for your routing tools
    assert os.getenv("GOOGLE_MAPS_API_KEY"), "Set GOOGLE_MAPS_API_KEY"

    # For Ollama, we just need a base URL + dummy API key
    # (OPENAI_API_KEY is only used because Autogen expects it)
    llm_config = {
        "config_list": [
            {
                "model": "llama3.2",  
                "api_key": os.getenv("OPENAI_API_KEY", "ollama"),
                "base_url": os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
            }
        ],
        "temperature": 0,
    }

    user = ConversableAgent(
        name="user",
        system_message="You are the user. Execute tools suggested by other agents.",
        llm_config=None,
        human_input_mode="NEVER",
    )

    route_agent = ConversableAgent(
        name="route_agent",
        system_message=(
            "You are a routing and road-safety specialist.\n"
            "\n"
            "When the user asks for routes and accident counts, ALWAYS call the tool\n"
            "`route_with_accidents(origin, destination, mode, buffer_meters)` exactly once.\n"
            "\n"
            "Arguments:\n"
            "- origin: full origin address string\n"
            "- destination: full destination address string\n"
            "- mode: 'driving' (use this unless user says otherwise)\n"
            "- buffer_meters: 50 if the user does not specify a different value.\n"
            "\n"
            "Do NOT write SQL or HTTP calls yourself. Do NOT say that you lack access\n"
            "to accident data: the tool `route_with_accidents` uses PostGIS and knows that.\n"
            "\n"
            "After calling the tool and getting its result, respond with:\n"
            "- route summary\n"
            "- total distance and duration (from the legs)\n"
            "- the encoded overview_polyline\n"
            "- the buffer_meters used\n"
            "- accident_count along the route\n"
            "\n"
            "IMPORTANT: You do NOT have access to weather data. Do NOT invent or hallucinate weather details.\n"
            "Leave weather reporting to the weather_agent.\n"
            "Only call the tool; do not invent code snippets in your final answer.\n"
            "At the end of your message, YOU MUST SAY: 'weather_agent, please fetch the weather for this route.'"
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    weather_agent = ConversableAgent(
        name="weather_agent",
        system_message=(
            "You are a weather specialist.\n"
            "Your ONLY goal is to fetch weather for the route.\n"
            "You have access to the tool `get_weather_for_last_route`.\n"
            "When asked to fetch weather, call this tool immediately.\n"
            "The tool takes NO arguments.\n"
            "\n"
            "EXAMPLE:\n"
            "User: ... fetch weather ...\n"
            "You: (Call tool get_weather_for_last_route())\n"
            "\n"
            "Do NOT summarize the route. Do NOT invent weather data.\n"
            "Do NOT say you cannot do it. Just call the tool."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Register tools
    route_tools = RouteAgentToolbox()
    route_tools.register(caller=route_agent, executor=user)

    weather_tools = WeatherAgentToolbox()
    weather_tools.register(caller=weather_agent, executor=user)

    # Group Chat
    groupchat = GroupChat(
        agents=[user, route_agent, weather_agent],
        messages=[],
        max_round=10,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    query = (
        "Get fastest driving route from '10 Carlson Ave, Clayton VIC' to '20 Kings College Dr, Bayswater VIC 3153'. "
        "Also fetch the weather along this route. "
        "Return: summary, leg distance/duration, overview polyline, accident count, and weather details."
    )
    
    result = user.initiate_chat(
        manager,
        message=query,
    )
    # print(result.summary) # GroupChatResult might not have summary attribute directly accessible like this in all versions, but usually it does or we check chat_history
