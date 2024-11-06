import requests
from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def get_location():
    # Code to retrieve location remains the same
    latitude = 22.7264
    longitude = 88.4753
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": f"{latitude},{longitude}",
        "key": "105ae62c16824b05955a777220824fdb",
        "pretty": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            components = data['results'][0]['components']
            city = components.get('city', '') or components.get('town', '') or components.get('suburb', '')
            postcode = "700124"
            state = components.get('state', '')
            country = components.get('country', '')
            location = f"{city}, Kolkata {postcode}, {state}, {country}"
            return location
    return None

def format_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        return time_obj.strftime("%I:%M %p")
    except ValueError:
        return time_str

def get_weather_response():
    location = get_location()
    if location is None:
        return "Could not retrieve location information."

    latitude = 22.7264
    longitude = 88.4753
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset,windspeed_10m_max,winddirection_10m_dominant",
        "timezone": "Asia/Kolkata"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return "Unable to retrieve the weather information at the moment."

    data = response.json()
    current_weather = data.get('current_weather', {})
    daily_weather = data.get('daily', {})

    # Format the response with weather details
    weather_info = f"Weather Information for {location} (Today):\n"
    weather_info += f"🌞 Current Temperature: {current_weather.get('temperature', 'N/A')} °C\n"
    weather_info += f"🔥 Max Temperature: {daily_weather.get('temperature_2m_max', ['N/A'])[0]} °C\n"
    weather_info += f"❄️ Min Temperature: {daily_weather.get('temperature_2m_min', ['N/A'])[0]} °C\n"
    weather_info += f"🌧️ Precipitation: {daily_weather.get('precipitation_sum', ['N/A'])[0]} mm\n"
    weather_info += f"🌅 Sunrise: {format_time(daily_weather.get('sunrise', ['N/A'])[0])}\n"
    weather_info += f"🌇 Sunset: {format_time(daily_weather.get('sunset', ['N/A'])[0])}\n"
    weather_info += f"🌬️ Wind Speed: {current_weather.get('windspeed', 'N/A')} km/h\n"
    weather_info += f"🧭 Wind Direction: {current_weather.get('winddirection', 'N/A')} degrees\n"

    # Forecast for the next 7 days
    weather_info += "\nForecast for the next 7 days:\n"
    for i in range(7):
        weather_info += f"\nDay {i + 1}:\n"
        weather_info += f"🔥 Max Temperature: {daily_weather.get('temperature_2m_max', ['N/A'])[i]} °C\n"
        weather_info += f"❄️ Min Temperature: {daily_weather.get('temperature_2m_min', ['N/A'])[i]} °C\n"
        weather_info += f"🌧️ Precipitation: {daily_weather.get('precipitation_sum', ['N/A'])[i]} mm\n"
        weather_info += f"🌅 Sunrise: {format_time(daily_weather.get('sunrise', ['N/A'])[i])}\n"
        weather_info += f"🌇 Sunset: {format_time(daily_weather.get('sunset', ['N/A'])[i])}\n"
        weather_info += f"🌬️ Wind Speed: {daily_weather.get('windspeed_10m_max', ['N/A'])[i]} km/h\n"
        weather_info += f"🧭 Wind Direction: {daily_weather.get('winddirection_10m_dominant', ['N/A'])[i]} degrees\n"
    
    return weather_info

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "weather" in incoming_msg:
        msg.body(get_weather_response())
    else:
        msg.body("Type 'weather' to get the latest weather information.")

    return str(resp)

if __name__ == "__main__":
    app.run()
