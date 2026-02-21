# models.py
import requests
import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
DB_PORT = os.getenv("DB_PORT")


class WeatherModel:
    def __init__(self):
        try:
            self.cache = redis.Redis(
                host=HOST, port=DB_PORT, db=0, decode_responses=True
            )
            self.cache.ping()
        except redis.ConnectionError:
            print("WARNING: Redis not found. The system is running without cache.")
            self.cache = None

        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

        self.icon_map = {
            "snow": "snowy",
            "rain": "showers",
            "fog": "fog",
            "wind": "windy",
            "cloudy": "cloudy",
            "partly-cloudy-day": "partly_cloudy",
            "partly-cloudy-night": "partly_cloudy",
            "clear-day": "sunny",
            "clear-night": "night",
            'rainy': 'rain',
            'night': 'clear',
            'day': 'clear',
        }

    def get_google_icon(self, vc_icon):
        icon_name = self.icon_map.get(vc_icon, "cloudy")
        return f"https://maps.gstatic.com/weather/v1/{icon_name}.svg"
        
    def get_uv_index(self, index):
        if index < 5: return "Low"
        if index < 7: return "Medium"
        return "High"

    def get_wind_description(self, speed):
        if speed < 1: return "Calm"
        if speed < 11: return "Light Breeze"
        if speed < 28: return "Moderate Wind"
        if speed < 49: return "Strong Wind"
        return "Wind"
    
    def get_wind_direction(self, degrees):
        directions = ['North', 'South', 'East', 'Southeast', 'South', 'South-west', 'West', 'Northwest']
        index = round(degrees / 45) % 8
        return directions[index]

    def get_weather(self, city):
        if self.cache:
            try:
                cached_data = self.cache.get(city)
                if cached_data:
                    print(f"Retrieving {city} from Redis cache.")
                    return json.loads(cached_data), "redis"
            except Exception as e:
                print(f"Error trying to get cache: {e}")

        print(f"Searching {city} on Weather API")
        url = f"{self.base_url}/{city}?key={self.api_key}&unitGroup=metric&include=days,current,hours"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 400:
                return {"error": "City not found or city name invalid."}, "error_city"

            if response.status_code in [401, 403]:
                return {"error": "Authentication error - API Key."}, "error_auth"

            response.raise_for_status()

            data = response.json()

            if self.cache:
                self.cache.set(city, json.dumps(data), ex=43200)

            return data, "weather_api"
        except requests.exceptions.ConnectionError:
            return {
                "error": "Unable to connect to the external weather service."
            }, "error_network"
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, "error_unknown"