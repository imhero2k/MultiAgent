import os
from autogen import ConversableAgent, UserProxyAgent
from weather_agent import WeatherAgentToolbox

# Mock LLM config (using the same as main.py)
llm_config = {
    "config_list": [{"model": "llama3.2", "base_url": os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1"), "api_key": "ollama"}],
    "cache_seed": None,  # Disable caching for testing
}

# Create Weather Agent (Exact copy of system message from main.py)
weather_agent = ConversableAgent(
    name="weather_agent",
    system_message=(
        "You are a weather agent. Your goal is to fetch weather for the route.\n"
        "You have access to the tool `get_weather_along_route`.\n"
        "When you see a route polyline in the chat history, call this tool.\n"
        "The tool takes one argument: `encoded_polyline`.\n"
        "Only call the tool; do not invent code snippets in your final answer.\n"
        "Do not summarize the route."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# Create User Proxy to simulate the Route Agent/User
user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
)

# Register tools
weather_tools = WeatherAgentToolbox()
weather_tools.register(caller=weather_agent, executor=user_proxy)

# Mock Polyline (short dummy)
mock_polyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"

# Initiate Chat
message = (
    "Here is the route summary.\n"
    f"POLYLINE: {mock_polyline}\n"
    "weather_agent, please fetch the weather for this route using the POLYLINE above."
)

print("Initiating chat with weather_agent...")
user_proxy.initiate_chat(
    weather_agent,
    message=message,
    max_turns=1
)
