import os
import requests
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a given city.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Error fetching weather: {data.get('message', 'Unknown error')}"

    description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    return (
        f"City: {city}\n"
        f"Condition: {description}\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {humidity}%"
    )
