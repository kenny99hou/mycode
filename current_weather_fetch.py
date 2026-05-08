import requests
import json
import time

# --- Configuration (CRITICAL: Replace these placeholders) ---

# 1. Get a free API key from a service like OpenWeatherMap.
# Example: API_KEY = "12345abcdef67890"
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY" 

# 2. Specify the location you want to check.
CITY_NAME = "London,UK" # Format: City,CountryCode (e.g., "Tokyo,JP")

# OpenWeatherMap API details
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

def get_current_weather(city, api_key):
    """
    Fetches the current weather data from the OpenWeatherMap API for a given city.
    """
    if api_key == "YOUR_OPENWEATHERMAP_API_KEY":
        print("ERROR: Please replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual key.")
        return None

    # Construct the full API request URL
    url = f"{BASE_URL}q={city}&appid={api_key}&units=metric" # units=metric for Celsius

    print(f"[{time.strftime('%H:%M:%S')}] Attempting to fetch weather data for {city}...")
    
    try:
        # Send the GET request to the API
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the city was found
        if data.get("cod") == "404":
            print(f"Error 404: City '{city}' not found.")
            return None

        return data

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from the API.")
    
    return None

def display_weather_data(weather_data):
    """
    Prints the key weather details in a readable format.
    """
    if not weather_data:
        return

    # Extract relevant data points
    city = weather_data['name']
    country = weather_data['sys']['country']
    temp_celsius = weather_data['main']['temp']
    feels_like_celsius = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description'].capitalize()
    wind_speed_mps = weather_data['wind']['speed'] # meters per second

    print("\n" + "="*40)
    print(f"Current Weather in {city}, {country}")
    print("="*40)
    print(f"Description: {description}")
    print(f"Temperature: {temp_celsius:.1f}°C")
    print(f"Feels Like:  {feels_like_celsius:.1f}°C")
    print(f"Humidity:    {humidity}%")
    print(f"Wind Speed:  {wind_speed_mps:.1f} m/s")
    print("="*40 + "\n")


if __name__ == "__main__":
    # Ensure 'requests' library is installed: pip install requests
    
    weather_info = get_current_weather(CITY_NAME, API_KEY)
    
    if weather_info:
        display_weather_data(weather_info)
    else:
        print("Failed to retrieve weather information.")
