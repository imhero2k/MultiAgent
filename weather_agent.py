from autogen.agentchat import ConversableAgent
import weather_tools as wt

class WeatherAgentToolbox:
    """
    Registers weather tools to Autogen agents.
    """
    def register(self, caller: ConversableAgent, executor: ConversableAgent) -> None:
        caller.register_for_llm(
            name="get_current_weather",
            description="Get current weather for a specific location (lat, lng).",
        )(wt.get_current_weather)
        executor.register_for_execution(name="get_current_weather")(wt.get_current_weather)

        caller.register_for_llm(
            name="get_weather_along_route",
            description="Get weather data for points along a route. Args: encoded_polyline (str). Returns a summary of weather conditions.",
        )(wt.get_weather_along_route)
        executor.register_for_execution(name="get_weather_along_route")(wt.get_weather_along_route)

        caller.register_for_llm(
            name="get_weather_for_last_route",
            description="Get weather for the most recently calculated route. No arguments required.",
        )(wt.get_weather_for_last_route)
        executor.register_for_execution(name="get_weather_for_last_route")(wt.get_weather_for_last_route)
