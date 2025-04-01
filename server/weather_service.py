# Import necessary libraries
from mcp.server.fastmcp import FastMCP
import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate an MCP server client
mcp = FastMCP("Weather Service MCP Server")

# Get API key from environment variables
# Note: You would need to create a .env file with your OpenWeatherMap API key
# API_KEY=your_openweathermap_api_key
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# DEFINE TOOLS

@mcp.tool()
def get_current_weather(city: str, units: str = "metric") -> Dict[str, Any]:
    """
    Get current weather for a city
    
    Args:
        city: City name (e.g., 'London', 'New York', 'Tokyo')
        units: Units of measurement ('metric' for Celsius, 'imperial' for Fahrenheit)
        
    Returns:
        Dictionary containing weather information
    """
    try:
        if not API_KEY:
            return {"error": "API key not found. Please set OPENWEATHER_API_KEY in .env file"}
        
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }
        
        response = httpx.get(f"{BASE_URL}/weather", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Format the response to be more user-friendly
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "clouds": data["clouds"]["all"],
            "units": units
        }
        
        return weather_info
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_weather_forecast(city: str, days: int = 5, units: str = "metric") -> Dict[str, Any]:
    """
    Get weather forecast for a city
    
    Args:
        city: City name (e.g., 'London', 'New York', 'Tokyo')
        days: Number of days for forecast (1-5)
        units: Units of measurement ('metric' for Celsius, 'imperial' for Fahrenheit)
        
    Returns:
        Dictionary containing forecast information
    """
    try:
        if not API_KEY:
            return {"error": "API key not found. Please set OPENWEATHER_API_KEY in .env file"}
        
        # Limit days to 1-5
        days = max(1, min(5, days))
        
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units,
            "cnt": days * 8  # API returns data in 3-hour intervals, so 8 per day
        }
        
        response = httpx.get(f"{BASE_URL}/forecast", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Format the response to be more user-friendly
        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": []
        }
        
        # Group forecast by day
        current_day = None
        day_forecast = None
        
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            
            if date != current_day:
                if day_forecast:
                    forecast["forecast"].append(day_forecast)
                
                current_day = date
                day_forecast = {
                    "date": date,
                    "intervals": []
                }
            
            interval = {
                "time": item["dt_txt"].split(" ")[1],
                "temperature": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "weather": item["weather"][0]["main"],
                "description": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"],
                "humidity": item["main"]["humidity"]
            }
            
            day_forecast["intervals"].append(interval)
        
        # Add the last day
        if day_forecast:
            forecast["forecast"].append(day_forecast)
        
        return forecast
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_air_pollution(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get air pollution data for a location
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        
    Returns:
        Dictionary containing air pollution information
    """
    try:
        if not API_KEY:
            return {"error": "API key not found. Please set OPENWEATHER_API_KEY in .env file"}
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }
        
        response = httpx.get(f"{BASE_URL}/air_pollution", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # AQI levels explanation
        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        
        components = data["list"][0]["components"]
        
        pollution_data = {
            "coordinates": {"lat": lat, "lon": lon},
            "aqi": data["list"][0]["main"]["aqi"],
            "aqi_description": aqi_levels[data["list"][0]["main"]["aqi"]],
            "components": {
                "co": components["co"],
                "no": components["no"],
                "no2": components["no2"],
                "o3": components["o3"],
                "so2": components["so2"],
                "pm2_5": components["pm2_5"],
                "pm10": components["pm10"],
                "nh3": components["nh3"]
            }
        }
        
        return pollution_data
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_geocoding(city: str) -> Dict[str, Any]:
    """
    Get geographical coordinates for a city
    
    Args:
        city: City name (e.g., 'London', 'New York', 'Tokyo')
        
    Returns:
        Dictionary containing geographical information
    """
    try:
        if not API_KEY:
            return {"error": "API key not found. Please set OPENWEATHER_API_KEY in .env file"}
        
        params = {
            "q": city,
            "appid": API_KEY,
            "limit": 1
        }
        
        response = httpx.get("http://api.openweathermap.org/geo/1.0/direct", params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return {"error": f"No location found for '{city}'"}
        
        location = data[0]
        
        geo_data = {
            "city": location.get("name"),
            "country": location.get("country"),
            "state": location.get("state"),
            "lat": location.get("lat"),
            "lon": location.get("lon")
        }
        
        return geo_data
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except Exception as e:
        return {"error": str(e)}

# DEFINE RESOURCES

@mcp.resource("weather://{city}")
def get_weather_resource(city: str) -> Dict[str, Any]:
    """
    Get weather as a resource
    
    Args:
        city: City name
        
    Returns:
        Weather information for the city
    """
    return get_current_weather(city)

# Execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")
